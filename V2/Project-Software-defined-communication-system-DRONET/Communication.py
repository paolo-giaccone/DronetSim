import random
import numpy as np

class Communication:
    def __init__(self, FES, gs, size_json, size_pkt, max_length_queue, N_UAVs, MAX_NUMB_OF_ATTEMPTIONS_TX_p0,
                 MAX_NUMB_OF_ATTEMPTIONS_TX_p1, data_analizer, Flag_double_ch):
        self.size_json = size_json
        self.size_pkt = size_pkt
        self.max_length_queue = max_length_queue

        self.N_UAVs = N_UAVs

        self.state_channel = 'idle'
        self.time_channel_is_getting_busy = 0
        self.time_channel_is_idle = 0

        self.cnt_iteration_per_each_UAV = np.zeros((self.N_UAVs + 1, 2))
        self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0 = MAX_NUMB_OF_ATTEMPTIONS_TX_p0
        self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1 = MAX_NUMB_OF_ATTEMPTIONS_TX_p1

        self.tot_pkt_lost = 0
        self.pkt_lost_interval_time = 0
        self.FES = FES

        self.gs = gs

        self.data_analizer = data_analizer

        self.flag_double_channel = Flag_double_ch

    def check_queue_availability(self, n_pkts_to_insert, UAV_sender_queue):
        # actual length of UAV
        len_queue = UAV_sender_queue.qsize()

        if len_queue + n_pkts_to_insert > self.max_length_queue:
            flag_pkts_can_be_inserted = False
        else:
            flag_pkts_can_be_inserted = True
        return flag_pkts_can_be_inserted

    def pkt_lost_register(self, UAV_sender, UAV_no_tx, cause_of_the_lost, tuple_test):
        if cause_of_the_lost == 'removed - congestion':
            if UAV_no_tx is not None:
                UAV_no_tx.pkt_lost_tot += 1
                UAV_no_tx.pkt_lost_queue_full += 1
            UAV_sender.pkt_lost_tot += 1
            UAV_sender.pkt_lost_queue_full += 1
        elif cause_of_the_lost == 'removed - expiration':
            if UAV_no_tx is not None:
                UAV_no_tx.pkt_lost_tot += 1
                UAV_no_tx.pkt_lost_iteration += 1
            UAV_sender.pkt_lost_tot += 1
            UAV_sender.pkt_lost_iteration += 1
        self.data_analizer.write_data_rx_pkt(tuple_test)

    def remove_pkts_expired_tx(self, UAV_sender, UAV_no_tx, sim_time, delta_msg_varying):
        # experied attempts tx -> remove pkt
        (gen_time, queue_owner, pkt_owner, pkt_type, size_pkt,
         priority_pkt, cnt_packet_sent, total_pkt, pkt_id) = UAV_sender.queue.get()
        state = 'removed - expiration'
        tuple_test = (
            sim_time, state, queue_owner, pkt_owner, pkt_type, size_pkt, priority_pkt, cnt_packet_sent, total_pkt,
            pkt_id, gen_time, None, None, None, delta_msg_varying)

        self.pkt_lost_register(UAV_sender, UAV_no_tx, state, tuple_test)

    def check_queue_empty(self, queue):
        if queue.empty():
            return True
        else:
            return False

    def sending_telemetry_data(self, UAV, relay, sim_time, delta_msg_varying):
        generation_pkt_time = sim_time
        cnt_packet_sent = numb_pkt = 1
        priority_of_pkt = 0
        pkt_owner = UAV.id
        type_pkt = 'json'
        pkt_id = UAV.pkt_id
        size_pkt = self.size_json

        pkt_tuple = (generation_pkt_time, 'queue', pkt_owner, type_pkt, size_pkt,
                     priority_of_pkt, cnt_packet_sent, numb_pkt, pkt_id)

        #needed for the starting of transmission
        flag_first_pkt_to_be_served = self.check_queue_empty(UAV.queue)

        #needed to check if there is enough space to insert the pkt
        flag_pkts_can_be_inserted = self.check_queue_availability(numb_pkt, UAV.queue)

        if flag_pkts_can_be_inserted:
            UAV.queue.put(pkt_tuple)
            print('The pkt of ID %d is inserted in the queue of: %s whose id is: %d size queue: %d' % (
                UAV.id, 'queue', UAV.id, UAV.queue.qsize()))
        else:
            cause_of_the_lost = 'removed - congestion'
            tuple_test = (
                sim_time, cause_of_the_lost, 'queue', pkt_owner, type_pkt, size_pkt, priority_of_pkt,
                cnt_packet_sent, numb_pkt,
                pkt_id, generation_pkt_time, None, None, None, delta_msg_varying)
            self.pkt_lost_register( UAV, None, cause_of_the_lost, tuple_test)
            print('The pkt of ID %d is NOT inserted in the queue of: %s whose id is: %d size queue: %d' % (
                UAV.id, 'queue', UAV.id, UAV.queue.qsize()))

        UAV.pkt_id += 1
        if flag_first_pkt_to_be_served:
            if UAV.bitrate > 0:
                print('ID: ', UAV.id, 'bitrate: ', UAV.bitrate, 'try to send telemetry data by myself')
                # check if the pkt freshly inserted is the first one in the pkt or there are others to be served
                    #      print('sending telemetry data: sim_time: ', sim_time )
                self.channel_communication(UAV, None, sim_time, delta_msg_varying)
            else:
                print('ID: ', UAV.id, 'bitrate: ', UAV.bitrate, 'try to send telemetry data by relay')
                print('the pkt of telemetry has to be sent toward the relay, size UAV queue: ', UAV.queue.qsize())
                self.bitrate_null_send_to_relay(UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt,
                                                priority_of_pkt)

    def sending_data_of_missings(self, UAV, relay, sim_time, delta_msg_varying):
        # size of the image has been chosen in function of the real images representing the mountains in 4K
        size_image = random.randint(1.5e4 * 8, 2e4 * 8)
        numb_pkt = np.ceil(size_image / self.size_pkt)
        priority_of_pkt = 0
        pkt_owner = UAV.id
        type_pkt = 'jpg'

        flag_first_pkt_to_be_served = self.check_queue_empty(UAV.queue)
        flag_pkts_can_be_inserted2 = True  # initialize the variable
        flag_pkts_can_be_inserted1 = self.check_queue_availability(numb_pkt + 1, UAV.queue)
        if not flag_pkts_can_be_inserted1:
            flag_pkts_can_be_inserted2 = self.check_queue_availability(1, UAV.queue)
            print('Check availability flag pkts can be inserted json P1: ', flag_pkts_can_be_inserted2)

        cnt = 1
        # insert or discard the image pkts
        while cnt <= numb_pkt:
            if size_image > self.size_pkt:
                size_pkt = self.size_pkt
            else:
                size_pkt = size_image

            if flag_pkts_can_be_inserted1:  # enough space to insert the whole image
                tuple_tx = (sim_time, 'queue', pkt_owner, type_pkt, size_pkt,
                            priority_of_pkt, cnt, numb_pkt, UAV.pkt_id)
                UAV.queue.put(tuple_tx)
            else:
                cause_of_the_lost = 'removed - congestion'
                tuple_test = (
                    sim_time, cause_of_the_lost, 'queue', pkt_owner, type_pkt, size_pkt, priority_of_pkt,
                    cnt, numb_pkt,
                    UAV.pkt_id, sim_time, None, None, None, delta_msg_varying)

                self.pkt_lost_register(UAV, None, cause_of_the_lost, tuple_test)
            #    print('The pkt jpg of ID %d is NOT inserted in the queue of: %s whose id is: %d size queue: %d' % (
            #       UAV.id, queue_owner, UAV_sender.id, UAV_sender.queue.qsize()))
            UAV.pkt_id += 1
            # decrease the image size
            size_image -= self.size_pkt
            cnt += 1

        if flag_pkts_can_be_inserted2:
            type_pkt = 'json'
        if flag_pkts_can_be_inserted2 or flag_pkts_can_be_inserted1:  # space only for one pkt - json
            tuple_tx = (sim_time, 'queue', pkt_owner, 'json', self.size_json,
                        1, 1, 1, UAV.pkt_id)
            UAV.queue.put(tuple_tx)
            # check if the pkt freshly inserted is the first one in the pkt or there are others to be served
            if flag_first_pkt_to_be_served:
                if UAV.bitrate > 0:
                    self.channel_communication(UAV, None, sim_time, delta_msg_varying )
                else:
                    if type_pkt == 'jpg':
                        priority_of_pkt = 0
                        size_pkt = self.size_pkt
                    else:
                        priority_of_pkt = 1
                        size_pkt = self.size_json
                    print('sending rescue data: inserted in the queue UAV whose length: ', UAV.queue.qsize(),
                          'and it has to be tx frmo relay')
                    self.bitrate_null_send_to_relay(UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt, priority_of_pkt)
        else:
            cause_of_the_lost = 'removed - congestion'
            tuple_test = (
                sim_time, cause_of_the_lost, 'queue', pkt_owner, 'json', self.size_json, 1,
                1, 1, UAV.pkt_id, sim_time, None, None, None, delta_msg_varying)
            self.pkt_lost_register(UAV, None, cause_of_the_lost, tuple_test)

    def bitrate_null_send_to_relay(self, UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt, priority_of_pkt):
        # if when was inserted the pkt the UAV had bitrate non null, and at
        # the new attempt tx is null -> send the pkt at the relay

        # check availability of relay queue
        flag_pkts_can_be_inserted = self.check_queue_availability(1, relay.queue)

        if flag_pkts_can_be_inserted:
            print('the transmission has to be done from the relay\n')
            self.tx_from_UAV_toward_RELAY(UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt, priority_of_pkt)
        else:
            cause_of_the_lost = 'removed - congestion'
            tmp = UAV.queue.get()
            (generation_pkt_time, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
             total_pkt, pkt_id) = tmp
            tuple_test = (
                sim_time, cause_of_the_lost, 'relay', pkt_owner, type_pkt, size_pkt, priority_of_pkt,
                cnt_packet_sent, total_pkt, pkt_id, generation_pkt_time, None, None, None, delta_msg_varying)
            self.pkt_lost_register(UAV, None, cause_of_the_lost, tuple_test)

    def tx_from_UAV_toward_RELAY(self, UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt, priority_of_pkt):
        print('we are in the function tx_from ...')
        if self.flag_double_channel:
            if relay.channel_relay == 'idle':
                relay.channel_relay = 'busy'
                UAV.im_tx_to_RELAY = True
                print('the channel relay is occupied : ', relay.channel_relay)
                tx_time = size_pkt / UAV.bitrate_Relay_UAV
                print('the tx_time for the second channel is  : ', tx_time)
                self.FES.add_events(sim_time + tx_time, 'Relay: Received pkt from UAV', UAV.id)

            else:
                print('ID: ', UAV.id, 'tx toward relay, the channnel is busy-> channel busy')
                self.channel_relay_busy(UAV, sim_time, type_pkt, size_pkt, priority_of_pkt, delta_msg_varying)
        else:
            if self.state_channel == 'idle':
                self.state_channel = 'busy'
                UAV.im_tx_to_RELAY = True
                print('the channel relay is occupied : ', relay.channel_relay)
                tx_time = size_pkt / UAV.bitrate_Relay_UAV
                print('the tx_time for the second channel is  : ', tx_time)
                self.FES.add_events(sim_time + tx_time, 'Relay: Received pkt from UAV', UAV.id)

            else:
                print('ID: ', UAV.id, 'tx toward relay, the channnel is busy-> channel busy')
                self.channel_relay_busy(UAV, sim_time, type_pkt, size_pkt, priority_of_pkt, delta_msg_varying)

    def channel_communication(self, UAV_sender, UAV_no_tx, sim_time, delta_msg_varying):
        # take the pkts from the queue
        tmp = UAV_sender.queue.get()
        (gen_time, queue_owner, pkt_owner, type_pkt, size_pkt,
         priority_of_pkt, cnt_packet_sent, total_pkt, pkt_id) = tmp
        if self.state_channel == 'idle':
            self.state_channel = 'busy'
            UAV_sender.im_tx_to_GS = True
            # computation of the tx time
            if UAV_sender.id == 0:
                tx_time = size_pkt / UAV_sender.drone.bitrate
            else:
                tx_time = size_pkt / UAV_sender.bitrate
            # prepare the event: Received data
            state = 'RECEIVED'
            identification = (
                gen_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
                total_pkt, pkt_id)
            self.FES.add_events(sim_time + tx_time, 'Received Data', identification)

            # remove the counter of the repetition of tx
            self.cnt_iteration_per_each_UAV[UAV_sender.id][0] = 0

            # scheduling another transmission of pkt belonging to the same UAV
            propagation_time = UAV_sender.distance_GS / 3e8
            identification1 = (UAV_sender.id, type_pkt, size_pkt, priority_of_pkt)
            if not UAV_sender.queue.empty() and type_pkt == 'jpg':
                # if there are other pkts composing the image
                # then the scheduling of the new event has a lower interval of time
                self.FES.add_events(sim_time + tx_time + propagation_time , 'Transmission attempt',identification1 )
            elif not UAV_sender.queue.empty() and type_pkt == 'json':
                rnd_wait = (random.uniform(0, (self.size_pkt * 8/ UAV_sender.bitrate)))
                self.FES.add_events(sim_time + tx_time + rnd_wait,'Transmission attempt', identification1 )

                print('\nrnd_wait: ', rnd_wait)
        elif self.state_channel == 'busy':
            UAV_sender.queue.put(tmp)
            self.channel_busy(UAV_sender, UAV_no_tx, priority_of_pkt, sim_time, delta_msg_varying, queue_owner,
                              type_pkt, size_pkt)
        else:
            print("ERROR: channel is neither busy nor idle")

    def channel_relay_busy(self, UAV, sim_time, type_pkt, size_pkt, priority_of_pkt, delta_msg_varying):
        drone_bitrate = UAV.bitrate_Relay_UAV
        event_to_schedule = 'Transmission attempt toward relay'
        identification = (UAV.id, type_pkt, size_pkt, priority_of_pkt)
        self.cnt_iteration_per_each_UAV[UAV.id][1] += 1

        if priority_of_pkt == 0:
            cnt_max_n_attemp = self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0
            rnd_wait = (random.uniform(0, (self.size_pkt * 8 / drone_bitrate) * 2 ** (
            (self.cnt_iteration_per_each_UAV[UAV.id][1] - 1))))

        else:
            cnt_max_n_attemp = self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1
            rnd_wait = (random.uniform(0, (self.size_pkt * 8 / drone_bitrate) ))

        if isinstance(rnd_wait, np.ndarray):
            rnd_wait = rnd_wait.item()

        print('\nrnd_wait: ', rnd_wait)

        # remove pkt cnt expired
        if self.cnt_iteration_per_each_UAV[UAV.id][1] >= cnt_max_n_attemp:
            print('CH2. ID: ', UAV.id, 'the pkt is removed\n')

            self.remove_pkts_expired_tx(UAV, None, sim_time, delta_msg_varying)
            self.cnt_iteration_per_each_UAV[UAV.id][1] = 0
            if not UAV.queue.empty():
                print('CH2. ID: ', UAV.id, 'the pkt is removed but a new pkt is inside the UAV -> schedule a new tx\n')
                self.FES.add_events(sim_time, event_to_schedule, identification)
        else:
            print('CH2. ID: ', UAV.id, 'the pkt is waiting for a new tx attempting in time: ', sim_time + rnd_wait, '\n')
            self.FES.add_events(sim_time + rnd_wait, event_to_schedule, identification)

    def channel_busy(self, UAV_sender, UAV_no_tx, priority_of_pkt, sim_time, delta_msg_varying, queue_owner, type_pkt, size_pkt):
        if queue_owner == 'queue':
            drone_bitrate = UAV_sender.bitrate
        else:
            drone_bitrate = UAV_sender.drone.bitrate
        if drone_bitrate == 0:
            drone_bitrate = random.uniform(UAV_sender.bitRate_max/4, UAV_sender.bitRate_max)

        identification = (UAV_sender.id, type_pkt, size_pkt, priority_of_pkt)
        self.cnt_iteration_per_each_UAV[UAV_sender.id][0] += 1

        if priority_of_pkt == 0:
            cnt_max_n_attemp = self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0
            rnd_wait = (random.uniform(0, (self.size_json * 8 / drone_bitrate) * 2 ** (
                (self.cnt_iteration_per_each_UAV[UAV_sender.id][0] - 1))))
        else:
            cnt_max_n_attemp = self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1
            rnd_wait = (random.uniform(0, (self.size_json * 8 / drone_bitrate)))

        if isinstance(rnd_wait, np.ndarray):
            rnd_wait = rnd_wait.item()

        print('\nrnd_wait: ', rnd_wait)

        # remove pkt cnt expired
        if self.cnt_iteration_per_each_UAV[UAV_sender.id][0] >= cnt_max_n_attemp:
            self.remove_pkts_expired_tx(UAV_sender, UAV_no_tx, sim_time, delta_msg_varying)
            self.cnt_iteration_per_each_UAV[UAV_sender.id][0] = 0
            if not UAV_sender.queue.empty():
                self.FES.add_events(sim_time, 'Transmission attempt', identification)
        else:
            self.FES.add_events(sim_time + rnd_wait, 'Transmission attempt', identification)

    def Relay_rx_pkt_from_UAV(self, UAV, relay, sim_time, delta_msg_varying):
        print('Im in the function Relay_rx_pkt_from_UAV')
        pkt = UAV.queue.get()
        print('Im in the function Relay_rx_pkt_from_UAV and ive taken the pkt')
        (generation_pkt_time, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
         total_pkt, pkt_id) = pkt

        # needed to check if there is enough space to insert the pkt
        flag_pkts_can_be_inserted = self.check_queue_availability(1, relay.queue)

        if flag_pkts_can_be_inserted:
            relay.queue.put(
                (generation_pkt_time, 'relay', pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
                 total_pkt, pkt_id))
            print('The pkt of ID %d is inserted in the queue of: %s whose id is: %d size queue: %d' % (
                relay.id, 'queue', relay.id, relay.queue.qsize()))
        else:
            cause_of_the_lost = 'removed - congestion'
            tuple_test = (
                sim_time, cause_of_the_lost, 'relay', pkt_owner, type_pkt, size_pkt, priority_of_pkt,
                cnt_packet_sent, None,
                pkt_id, generation_pkt_time, None, None, None, delta_msg_varying)
            self.pkt_lost_register(UAV, None, cause_of_the_lost, tuple_test)
            print('The pkt of ID %d is NOT inserted in the queue of: %s whose id is: %d size queue: %d' % (
                UAV.id, 'relay', UAV.id, UAV.queue.qsize()))

        self.cnt_iteration_per_each_UAV[UAV.id][1] = 0
        if self.flag_double_channel:
            relay.channel_relay = 'idle'
        else:
            self.state_channel = 'idle'

        UAV.im_tx_to_RELAY = False
        # if it is the first to be served, then try to tx
        if relay.queue.qsize() == 1:
            self.channel_communication(relay, UAV, sim_time, delta_msg_varying)

        # check if the UAV with the null bit rate has other pkts in the queue
        # if it is so -> then try to rescedule the tx for this new pkt considering the possibility that if it is moving -> the bit rate is no more null
        if UAV.queue.qsize() >= 1:
            propagation_time = relay.distance_relay_UAV / 3e8
            identification = (UAV.id, type_pkt, size_pkt, priority_of_pkt)
            if type_pkt == 'jpg':
                self.FES.add_events(sim_time + propagation_time * 1e2,
                                    'Transmission attempt toward relay', identification)
            else:
                rnd_wait = (random.uniform(0, (self.size_pkt * 8/ UAV.bitrate_Relay_UAV)))
                self.FES.add_events(sim_time + rnd_wait,
                                    'Transmission attempt toward relay', identification)
                print('CH2. meanwhile the tx: ive schedulated a new tx attempt for relay in time: ',
                  sim_time + rnd_wait)
                print('rnd_wait: ', rnd_wait)

    def received_data(self, identification, UAV_tx, sim_time, delta_msg_varying):
        (gen_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
         total_pkt, pkt_id) = identification

        if type_pkt == 'jpg':
            UAV_tx.pkt_cnt_jpg += 1
            if UAV_tx.pkt_cnt_jpg != total_pkt + 1:
                if UAV_tx.pkt_cnt_jpg == 1: # cera 0
                    UAV_tx.start_tx_jpg = gen_time
                #print('\n pkt cnt_jpg = ', UAV_tx.pkt_cnt_jpg, 'total pkt: ', total_pkt)
                UAV_tx.total_latency_pkt = None
            else:
                UAV_tx.pkt_cnt_jpg = 0
                UAV_tx.total_latency_pkt = sim_time - gen_time
        else:
            UAV_tx.total_latency_pkt = sim_time - gen_time

        tuple_test = (
            sim_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
            total_pkt, pkt_id, gen_time, sim_time, None, UAV_tx.total_latency_pkt, delta_msg_varying)

        self.data_analizer.write_data_rx_pkt(tuple_test)
        self.gs.buffer.put(
            (sim_time, gen_time, queue_owner, pkt_owner, priority_of_pkt, type_pkt, cnt_packet_sent, total_pkt))
        self.gs.receive()

        self.state_channel = 'idle'
        UAV_tx.im_tx_to_GS = False