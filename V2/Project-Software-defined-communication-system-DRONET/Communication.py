import random
import numpy as np

class Communication:
    def __init__(self, FES, gs, size_json, size_pkt, max_length_queue, N_UAVs, MAX_NUMB_OF_ATTEMPTIONS_TX_p0,
                 MAX_NUMB_OF_ATTEMPTIONS_TX_p1, data_analizer, Flag_double_ch):
        self.size_json = size_json
        self.size_pkt = size_pkt
        self.max_length_queue = max_length_queue

        self.N_UAVs = N_UAVs

        #channel used for the communication toward the GS
        self.state_channel = 'idle'

        #counter that takes into account the tx attemptions of each single UAV
        self.cnt_iteration_per_each_UAV = np.zeros((self.N_UAVs + 1, 2))

        self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0 = MAX_NUMB_OF_ATTEMPTIONS_TX_p0
        self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1 = MAX_NUMB_OF_ATTEMPTIONS_TX_p1

        self.FES = FES

        self.gs = gs

        self.data_analizer = data_analizer

        #flag that indicatates if the communication uses a double channel or a single one
        self.flag_double_channel = Flag_double_ch

    #function used to check if there is enough space on the queue
    def check_queue_availability(self, n_pkts_to_insert, UAV_sender_queue):
        # actual length of UAV
        len_queue = UAV_sender_queue.qsize()

        if len_queue + n_pkts_to_insert > self.max_length_queue:
            flag_pkts_can_be_inserted = False
        else:
            flag_pkts_can_be_inserted = True
        return flag_pkts_can_be_inserted

    #if a pkt has to be removed, then by calling this function, it register the state of removed pkt in the csv file
    # (it calls the function 'self.data_analizer.write_data_rx_pkt(tuple_test)'
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

    #function used if the pkt has exhausted its transmission attempts -> this followinf function is called
    #it basically creates the tuple that is passed to the pkt_lost_register function
    def remove_pkts_expired_tx(self, UAV_sender, UAV_no_tx, sim_time, delta_msg_varying):
        # experied attempts tx -> remove pkt
        (gen_time, queue_owner, pkt_owner, pkt_type, size_pkt,
         priority_pkt, cnt_packet_sent, total_pkt, pkt_id) = UAV_sender.queue.get()
        state = 'removed - expiration'
        tuple_test = (
            sim_time, state, queue_owner, pkt_owner, pkt_type, size_pkt, priority_pkt, cnt_packet_sent, total_pkt,
            pkt_id, gen_time, None, None, None, delta_msg_varying)

        self.pkt_lost_register(UAV_sender, UAV_no_tx, state, tuple_test)

    #check if the queue is empty or not
    def check_queue_empty(self, queue):
        if queue.empty():
            return True
        else:
            return False

    #function that is used for the transmission of the synchrounous data
    def sending_telemetry_data(self, UAV, relay, sim_time, delta_msg_varying):
        generation_pkt_time = sim_time #time at which the pkt is generated
        cnt_packet_sent = numb_pkt = 1 #1 = only one pkt is sent (size of the json is smaller than a single pkt)
        priority_of_pkt = 0
        pkt_owner = UAV.id  #store the ID of the UAV that has to tx
        type_pkt = 'json'
        pkt_id = UAV.pkt_id #store the ID of the pkt that has to tx
        size_pkt = self.size_json

        #creates the pkt that contains the following parameters
        pkt_tuple = (generation_pkt_time, 'queue', pkt_owner, type_pkt, size_pkt,
                     priority_of_pkt, cnt_packet_sent, numb_pkt, pkt_id)

        #needed for the starting of transmission
        flag_first_pkt_to_be_served = self.check_queue_empty(UAV.queue)

        #needed to check if there is enough space to insert the pkt
        flag_pkts_can_be_inserted = self.check_queue_availability(numb_pkt, UAV.queue)

        if flag_pkts_can_be_inserted: #then insert the pkt in the queue
            UAV.queue.put(pkt_tuple)
        else:
            cause_of_the_lost = 'removed - congestion'  #congestion of the queue
            tuple_test = (  #creates the tuple containg all the parameters that have to be reported con the csv file
                sim_time, cause_of_the_lost, 'queue', pkt_owner, type_pkt, size_pkt, priority_of_pkt,
                cnt_packet_sent, numb_pkt,
                pkt_id, generation_pkt_time, None, None, None, delta_msg_varying)
            self.pkt_lost_register( UAV, None, cause_of_the_lost, tuple_test)   #registration of the pkt lost


        UAV.pkt_id += 1 #indicates the ID of the new pkt that will be generated

        if flag_first_pkt_to_be_served:#check if before of insert the data there were presents other pkts waitng for their transmission
            if UAV.bitrate > 0: #send directly toward the GS
                print('ID: ', UAV.id, 'bitrate: ', UAV.bitrate, 'try to send telemetry data by myself')
                self.channel_communication(UAV, None, sim_time, delta_msg_varying)
            else:
                self.bitrate_null_send_to_relay(UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt,
                                                priority_of_pkt)    #the transmission has one hop, first tx toward the relè and in time will tx toward the GS

    def sending_data_of_missings(self, UAV, relay, sim_time, delta_msg_varying):    #sending the asynchronous pkts
        # size of the image has been chosen in function of the real images representing the mountains in 4K
        size_image = random.randint(1.5e4 * 8, 2e4 * 8) #size of the image
        numb_pkt = np.ceil(size_image / self.size_pkt)  #computes the number of pkts containg the whole image
        priority_of_pkt = 0 #image has priority 0
        pkt_owner = UAV.id
        type_pkt = 'jpg'

        flag_first_pkt_to_be_served = self.check_queue_empty(UAV.queue) #check if the pkts that have to be inserted are the first ones to be tx

        flag_pkts_can_be_inserted1 = self.check_queue_availability(numb_pkt + 1, UAV.queue) #check if there is enough space in the queue for containg the whole image + json file

        flag_pkts_can_be_inserted2 = self.check_queue_availability(1, UAV.queue)           #  flag_pkts_can_be_inserted2 = self.check_queue_availability(1, UAV.queue)

        cnt = 1 #counter needed for the counting of the pkts for the image
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
                cause_of_the_lost = 'removed - congestion'  #else register the pkts lsot due to the congested queue
                tuple_test = (
                    sim_time, cause_of_the_lost, 'queue', pkt_owner, type_pkt, size_pkt, priority_of_pkt,
                    cnt, numb_pkt,
                    UAV.pkt_id, sim_time, None, None, None, delta_msg_varying)

                self.pkt_lost_register(UAV, None, cause_of_the_lost, tuple_test)
            #    print('The pkt jpg of ID %d is NOT inserted in the queue of: %s whose id is: %d size queue: %d' % (
            #       UAV.id, queue_owner, UAV_sender.id, UAV_sender.queue.qsize()))
            UAV.pkt_id += 1 #set the new id for the incoming pkt
            # decrease the image size
            size_image -= self.size_pkt
            cnt += 1

        if flag_pkts_can_be_inserted2 or flag_pkts_can_be_inserted1:  #if there space for at least the pkt of json, the insert it
            type_pkt = 'json'
            tuple_tx = (sim_time, 'queue', pkt_owner, 'json', self.size_json,
                        1, 1, 1, UAV.pkt_id)
            UAV.queue.put(tuple_tx) #inser the pkt
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

                    #if bitrate null -> use the relay
                    self.bitrate_null_send_to_relay(UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt, priority_of_pkt)
        else:#if there is no enough space for the coordinate file, then register it
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

        if flag_pkts_can_be_inserted: #if true-> the transmission has to be done from the relay
            self.tx_from_UAV_toward_RELAY(UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt, priority_of_pkt)
        else:#register the pkt lost
            cause_of_the_lost = 'removed - congestion'
            tmp = UAV.queue.get()
            (generation_pkt_time, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
             total_pkt, pkt_id) = tmp
            tuple_test = (
                sim_time, cause_of_the_lost, 'relay', pkt_owner, type_pkt, size_pkt, priority_of_pkt,
                cnt_packet_sent, total_pkt, pkt_id, generation_pkt_time, None, None, None, delta_msg_varying)
            self.pkt_lost_register(UAV, None, cause_of_the_lost, tuple_test)

    def tx_from_UAV_toward_RELAY(self, UAV, relay, sim_time, delta_msg_varying, type_pkt, size_pkt, priority_of_pkt):
        if self.flag_double_channel: #if we want to use a double channel
            if relay.channel_relay == 'idle': #schedule the reception of the packet at the relay
                relay.channel_relay = 'busy'
              #  UAV.im_tx_to_RELAY = True   #used later for distinguish the communication
                tx_time = size_pkt / UAV.bitrate_Relay_UAV  #compute the transmission time
                self.FES.add_events(sim_time + tx_time, 'Relay: Received pkt from UAV', UAV.id)

            else:
                self.channel_relay_busy(UAV, sim_time, type_pkt, size_pkt, priority_of_pkt, delta_msg_varying) #channel busy
        else: #if we want use the same channel for the tx of the GS ->do the same operation by using the same channel
            if self.state_channel == 'idle':
                self.state_channel = 'busy'
               # UAV.im_tx_to_RELAY = True
                print('the channel relay is occupied : ', relay.channel_relay)
                tx_time = size_pkt / UAV.bitrate_Relay_UAV
                print('the tx_time for the second channel is  : ', tx_time)
                self.FES.add_events(sim_time + tx_time, 'Relay: Received pkt from UAV', UAV.id)

            else:
                print('ID: ', UAV.id, 'tx toward relay, the channnel is busy-> channel busy')
                self.channel_relay_busy(UAV, sim_time, type_pkt, size_pkt, priority_of_pkt, delta_msg_varying)

    def channel_communication(self, UAV_sender, UAV_no_tx, sim_time, delta_msg_varying):    #function used for the transmission
        # take the pkts from the queue
        tmp = UAV_sender.queue.get()
        (gen_time, queue_owner, pkt_owner, type_pkt, size_pkt,
         priority_of_pkt, cnt_packet_sent, total_pkt, pkt_id) = tmp #take the pkt that has to be transmitted
        if self.state_channel == 'idle':
            self.state_channel = 'busy' #occupy the channel
           # UAV_sender.im_tx_to_GS = True   #indicate that the transmission is
            # computation of the tx time
            if UAV_sender.id == 0:
                tx_time = size_pkt / UAV_sender.drone.bitrate
            else:
                tx_time = size_pkt / UAV_sender.bitrate
            # prepare the event: Received data
            state = 'RECEIVED'
            identification = (
                gen_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
                total_pkt, pkt_id)  #parameters needed for the reception
            self.FES.add_events(sim_time + tx_time, 'Received Data', identification)    #schedule the reception of the file

            # remove the counter of the repetition of tx
            self.cnt_iteration_per_each_UAV[UAV_sender.id][0] = 0   #reset the counter of tx attempts

            # scheduling another transmission of pkt belonging to the same UAV
            propagation_time = UAV_sender.distance_GS / 3e8 #compute the propagation time
            identification1 = (UAV_sender.id, type_pkt, size_pkt, priority_of_pkt)  #parameters needed for the scheduling of the new tx pkt
            if not UAV_sender.queue.empty() and type_pkt == 'jpg':  #if the nearly senses pkt is jpg: then schedule the new tx of the pkt in a limited amount of time
                # if there are other pkts composing the image
                # then the scheduling of the new event has a lower interval of time
                self.FES.add_events(sim_time + tx_time + propagation_time , 'Transmission attempt',identification1 )
            elif not UAV_sender.queue.empty() and type_pkt == 'json':   #else if is present a pkt json, schedule the tx in a large rnd_wait interval
                rnd_wait = (random.uniform(0, (self.size_pkt * 8/ UAV_sender.bitrate)))
                self.FES.add_events(sim_time + tx_time + rnd_wait,'Transmission attempt', identification1 )

                print('\nrnd_wait: ', rnd_wait)
        elif self.state_channel == 'busy':  #if the channel is busy, then try to send later on
            UAV_sender.queue.put(tmp)   #re-insert the pkt in the queue
            self.channel_busy(UAV_sender, UAV_no_tx, priority_of_pkt, sim_time, delta_msg_varying, queue_owner,
                              type_pkt, size_pkt)
        else:
            print("ERROR: channel is neither busy nor idle")

    def channel_relay_busy(self, UAV, sim_time, type_pkt, size_pkt, priority_of_pkt, delta_msg_varying):    #used only for the transmission oward the relay
        drone_bitrate = UAV.bitrate_Relay_UAV   #store the bitrate of the UAV
        event_to_schedule = 'Transmission attempt toward relay'
        identification = (UAV.id, type_pkt, size_pkt, priority_of_pkt)
        self.cnt_iteration_per_each_UAV[UAV.id][1] += 1 #incresed the tx attempt

        #initializes the different parameters in function of the priority
        if priority_of_pkt == 0:
            cnt_max_n_attemp = self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0
            rnd_wait = (random.uniform(0, (self.size_pkt * 8 / drone_bitrate) * 2 ** (
            (self.cnt_iteration_per_each_UAV[UAV.id][1] - 1))))

        else:
            cnt_max_n_attemp = self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1
            rnd_wait = (random.uniform(0, (self.size_pkt * 8 / drone_bitrate) ))

        if isinstance(rnd_wait, np.ndarray):
            rnd_wait = rnd_wait.item()

        # remove pkt cnt expired
        if self.cnt_iteration_per_each_UAV[UAV.id][1] >= cnt_max_n_attemp:  #expired tx attemptions

            self.remove_pkts_expired_tx(UAV, None, sim_time, delta_msg_varying) #remove the pkt
            self.cnt_iteration_per_each_UAV[UAV.id][1] = 0  #reset the coutnr
            if not UAV.queue.empty():   #if the queue is not empty try to schedule the tx of the pkt
                print('CH2. ID: ', UAV.id, 'the pkt is removed but a new pkt is inside the UAV -> schedule a new tx\n')
                self.FES.add_events(sim_time, event_to_schedule, identification)
        else:   #if it is not expired -> then try to re-sent it later
            print('CH2. ID: ', UAV.id, 'the pkt is waiting for a new tx attempting in time: ', sim_time + rnd_wait, '\n')
            self.FES.add_events(sim_time + rnd_wait, event_to_schedule, identification)

    def channel_busy(self, UAV_sender, UAV_no_tx, priority_of_pkt, sim_time, delta_msg_varying, queue_owner, type_pkt, size_pkt):
        if queue_owner == 'queue':
            drone_bitrate = UAV_sender.bitrate
        else:
            drone_bitrate = UAV_sender.drone.bitrate
        if drone_bitrate == 0:
            drone_bitrate = random.uniform(UAV_sender.bitRate_max/4, UAV_sender.bitRate_max)    #it is used only for the computation of the rnd_wait (is impossible that the UAV will tx the pkt on it's own)

        identification = (UAV_sender.id, type_pkt, size_pkt, priority_of_pkt)
        self.cnt_iteration_per_each_UAV[UAV_sender.id][0] += 1  #increase the counter

        if priority_of_pkt == 0:
            cnt_max_n_attemp = self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0   #tx attemps < then the one with higher priority
            rnd_wait = (random.uniform(0, (self.size_json * 8 / drone_bitrate) * 2 ** (
                (self.cnt_iteration_per_each_UAV[UAV_sender.id][0] - 1))))  #compute rnd_wait
        else:
            cnt_max_n_attemp = self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1
            rnd_wait = (random.uniform(0, (self.size_json * 8 / drone_bitrate)))

        if isinstance(rnd_wait, np.ndarray):
            rnd_wait = rnd_wait.item()

        print('\nrnd_wait: ', rnd_wait)

        # remove pkt cnt expired
        if self.cnt_iteration_per_each_UAV[UAV_sender.id][0] >= cnt_max_n_attemp:   #expired time
            self.remove_pkts_expired_tx(UAV_sender, UAV_no_tx, sim_time, delta_msg_varying) #remove the pkt
            self.cnt_iteration_per_each_UAV[UAV_sender.id][0] = 0   #reset the counter
            if not UAV_sender.queue.empty():
                self.FES.add_events(sim_time, 'Transmission attempt', identification)
        else:
            self.FES.add_events(sim_time + rnd_wait, 'Transmission attempt', identification)

    def Relay_rx_pkt_from_UAV(self, UAV, relay, sim_time, delta_msg_varying):
        pkt = UAV.queue.get()       #function related on the reception of the pkt in the relay

        (generation_pkt_time, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
         total_pkt, pkt_id) = pkt

        # needed to check if there is enough space to insert the pkt
        flag_pkts_can_be_inserted = self.check_queue_availability(1, relay.queue)   #check if there is space in the queue

        if flag_pkts_can_be_inserted:
            relay.queue.put(
                (generation_pkt_time, 'relay', pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
                 total_pkt, pkt_id))    #if there is space, then insert it in the queue

        else:
            cause_of_the_lost = 'removed - congestion'  #else store in the csv the pkt lost
            tuple_test = (
                sim_time, cause_of_the_lost, 'relay', pkt_owner, type_pkt, size_pkt, priority_of_pkt,
                cnt_packet_sent, None,
                pkt_id, generation_pkt_time, None, None, None, delta_msg_varying)
            self.pkt_lost_register(UAV, None, cause_of_the_lost, tuple_test)
            print('The pkt of ID %d is NOT inserted in the queue of: %s whose id is: %d size queue: %d' % (
                UAV.id, 'relay', UAV.id, UAV.queue.qsize()))

        self.cnt_iteration_per_each_UAV[UAV.id][1] = 0  #reset the counter of the tx
        if self.flag_double_channel:    #douvble channel
            relay.channel_relay = 'idle'
        else:   #single channel
            self.state_channel = 'idle'

       # UAV.im_tx_to_RELAY = False
        # if it is the first to be served, then try to tx
        if relay.queue.qsize() == 1:
            self.channel_communication(relay, UAV, sim_time, delta_msg_varying) #if there is only the early pkt inserted in the queue, try to send it

        # check if the UAV with the null bit rate has other pkts in the queue
        # if it is so -> then try to rescedule the tx for this new pkt considering the possibility that if it is moving -> the bit rate is no more null
        if UAV.queue.qsize() >= 1:  #if the size of the queue of the UAV contains other pkts, then try to send them towaard the relay
            propagation_time = relay.distance_relay_UAV / 3e8
            identification = (UAV.id, type_pkt, size_pkt, priority_of_pkt)
            if type_pkt == 'jpg':   #send faster the other jpg pkts
                self.FES.add_events(sim_time + propagation_time,
                                    'Transmission attempt toward relay', identification)
            else:   #contand the channel as the other UAVs
                rnd_wait = (random.uniform(0, (self.size_pkt * 8/ UAV.bitrate_Relay_UAV)))
                self.FES.add_events(sim_time + rnd_wait,
                                    'Transmission attempt toward relay', identification)

    def received_data(self, identification, UAV_tx, sim_time, delta_msg_varying):
        (gen_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
         total_pkt, pkt_id) = identification

        #needed for the computetion of the latency of the whole image
        if type_pkt == 'jpg':
            UAV_tx.pkt_cnt_jpg += 1 #counts the received pkts
            if UAV_tx.pkt_cnt_jpg != total_pkt + 1:
                if UAV_tx.pkt_cnt_jpg == 1: #
                    UAV_tx.start_tx_jpg = gen_time

                UAV_tx.total_latency_pkt = None
            else:
                UAV_tx.pkt_cnt_jpg = 0
                UAV_tx.total_latency_pkt = sim_time - gen_time
        else:
            UAV_tx.total_latency_pkt = sim_time - gen_time

        #register the received pkt in the csv file
        tuple_test = (
            sim_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
            total_pkt, pkt_id, gen_time, sim_time, None, UAV_tx.total_latency_pkt, delta_msg_varying)

        self.data_analizer.write_data_rx_pkt(tuple_test)
        #insert the received pkt in the queeu
        self.gs.buffer.put(
            (sim_time, gen_time, queue_owner, pkt_owner, priority_of_pkt, type_pkt, cnt_packet_sent, total_pkt))
        self.gs.receive()

        self.state_channel = 'idle'
        #UAV_tx.im_tx_to_GS = False