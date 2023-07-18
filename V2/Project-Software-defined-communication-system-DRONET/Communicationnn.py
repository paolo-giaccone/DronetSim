from FES_management import FES_management
import random
import numpy as np
import queue

from DataAnalizer import data_analizer

class Communicatklkòion:
    def __init__(self, FES, gs, size_json, size_pkt, max_length_queue, N_UAVs, MAX_NUMB_OF_ATTEMPTIONS_TX_p0,
                 MAX_NUMB_OF_ATTEMPTIONS_TX_p1, data_analizer):
        self.size_json = size_json
        self.size_pkt = size_pkt
        self.max_length_queue = max_length_queue

        self.N_UAVs = N_UAVs

        self.state_channel = 'idle'
        self.time_channel_is_getting_busy = 0
        self.time_channel_is_idle = 0

        self.cnt_iteration_per_each_UAV = np.zeros((self.N_UAVs + 1, 1))
        self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0 = MAX_NUMB_OF_ATTEMPTIONS_TX_p0
        self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1 = MAX_NUMB_OF_ATTEMPTIONS_TX_p1

        self.tot_pkt_lost = 0
        self.pkt_lost_interval_time = 0
        self.FES = FES

        self.gs = gs

        self.data_analizer = data_analizer

    def telemetry_insertion(self, UAV_sender, UAV_no_tx, pkt_tuple, sim_time):
        # check if the queue is empty
        if UAV_sender.queue.empty():
            flag_queue_empty = True
        else:
            flag_queue_empty = False

        (generation_pkt_time, queue_owner, pkt_owner, priority_of_pkt, type_pkt, pkt_id, size_pkt, cnt, numb_pkt,
         ) = pkt_tuple
        # check if the queue of the UAV is full
        if UAV_sender.queue.full():
            state = 'removed congested queue'
            queue_owner = 'relay'
            tuple_test = (
                generation_pkt_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt, numb_pkt,
                pkt_id, generation_pkt_time, None, None, None)
            self.data_analizer.write_data_rx_pkt(tuple_test) #is used for the test and validation

            UAV_sender.pkt_lost_tot += 1
            UAV_sender.pkt_lost_json += 1
            UAV_sender.pkt_lost_queue_full += 1
            if UAV_no_tx is not None:
                UAV_no_tx.pkt_lost_tot += 1
                UAV_no_tx.pkt_lost_json += 1
                UAV_no_tx.pkt_lost_queue_full += 1
            self.tot_pkt_lost += size_pkt
            self.pkt_lost_interval_time += size_pkt
            print('\nTelemetry\nDrone: ', UAV_sender.id, 'the queue is full and none telemetry pkt has been inserted\n')
        else:
            UAV_sender.queue.put((generation_pkt_time, queue_owner, pkt_owner, type_pkt, size_pkt,
                                  priority_of_pkt, cnt, numb_pkt, pkt_id))
            print('\nTelemetry\nDrone: ', UAV_sender.id,
                  'a tel. pkt has been inserted in the queue\n')
            print('\n SimTime: ', sim_time, '\n Drone: ', UAV_sender.id,
                  '\n Size Queue: ', UAV_sender.queue.qsize(), '\n Bitrate: ', UAV_sender.bitrate, '\n')

            if flag_queue_empty:
                self.channel_communication(UAV_sender, UAV_no_tx, sim_time)

    def sending_periodic_data(self, drone, relay, sim_time ):

        # parameters of the new pkt
        cnt = 1
        numb_pkt = 1
        type_pkt = 'json'
        priority_pkt = 0
        drone.pkt_id += 1
        pkt_owner = drone.id

        #check if the bitrate is null
        if drone.bitrate == 0:
            queue_owner = 'relay'
            UAV_sender = relay
            UAV_no_tx = drone
        else:
            queue_owner = 'queue'
            UAV_sender = drone
            UAV_no_tx = None

        # creation of a tuple to be sent in the queue
        tuple = (( sim_time, queue_owner, pkt_owner, priority_pkt,type_pkt, drone.pkt_id, self.size_json,
                  cnt, numb_pkt ))
        self.telemetry_insertion(UAV_sender, UAV_no_tx, tuple, sim_time)

    def sending_data_of_the_rescue(self, drone, relay, sim_time):

        # size of the image has been chosen in function of the real images representing the mountains in 4K
        size_image = random.randint(1.5e4 * 8, 2e4 * 8)
        numb_pkt = np.ceil(size_image / self.size_pkt)
        priority_of_pkt = 0

        # check if the bitrate is null
        if drone.bitrate == 0:
            queue_owner = 'relay'
            UAV_sender = relay
            UAV_no_tx = drone
        else:
            queue_owner = 'queue'
            UAV_sender = drone
            UAV_no_tx = None

        # check the queue
        self.check_queue(UAV_sender, UAV_no_tx, sim_time)

        # check if the queue is empty before the insertion of new pkts
        if UAV_sender.queue.empty():
            flag_queue_empty = True
        else:
            flag_queue_empty = False

        # controllo se all' interno della queue c'è spazio a sufficienza per inserire tutti i pkt jpg+json
        if (UAV_sender.queue.qsize() + numb_pkt + 1) > self.max_length_queue:
            flag_send_just_json = 1
            print('Drone: ', UAV_sender.id, 'there is no space to locate all the pkts')
        else:
            # there is enough space to locate all the pkts json+jpg
            flag_send_just_json = 0
            print('Drone: ', UAV_sender.id, 'there is enough space to locate all the pkts')

        cnt = 1  # contatore dei pacchetti del jpg file
        if flag_send_just_json == 0:  # enough space to locate all the pkts json+jpg
            while cnt <= numb_pkt:
                if size_image > self.size_pkt:
                    type_pkt = 'jpg'
                    size_pkt = self.size_pkt
                else:
                    type_pkt = 'jpg'
                    size_pkt = size_image
                UAV_sender.queue.put(
                    (sim_time, queue_owner, drone.id, type_pkt, size_pkt,
                     priority_of_pkt, cnt, numb_pkt, drone.pkt_id))
                drone.pkt_id += 1
                # decrease the image size
                size_image -= self.size_pkt
                cnt += 1
        else:
            # register all the jpg that have been lost due to the queue congestion
            while cnt <= numb_pkt:
                type_pkt = 'jpg'
                state = 'removed congested queue'
                UAV_sender.pkt_lost_tot += 1
                UAV_sender.pkt_lost_jpg += 1
                UAV_sender.pkt_lost_queue_full += 1

                if UAV_no_tx is not None:
                    UAV_no_tx.pkt_lost_tot += 1
                    UAV_no_tx.pkt_lost_jpg += 1
                    UAV_no_tx.pkt_lost_queue_full += 1

                if size_image > self.size_pkt:
                    size_file = self.size_pkt
                else:
                    size_file = size_image
                drone.pkt_id += 1
                size_image -= self.size_pkt
                cnt += 1

                tuple_test = (
                    sim_time, state, queue_owner, drone.id, type_pkt, size_file, priority_of_pkt, cnt, numb_pkt,
                    drone.pkt_id, sim_time, None, None, None)
                self.data_analizer.write_data_rx_pkt(tuple_test)

        if UAV_sender.queue.full():
            print('EIIIIII IS FULLLLL')
            UAV_sender.pkt_lost_P1 += 1
            UAV_sender.pkt_lost_tot += 1
            UAV_sender.pkt_lost_queue_full += 1
            if UAV_no_tx is not None:
                UAV_no_tx.pkt_lost_tot += 1
                UAV_no_tx.pkt_lost_P1 += 1
                UAV_no_tx.pkt_lost_queue_full += 1
            tuple_test = (
                sim_time, state, queue_owner, drone.id, type_pkt, size_file, priority_of_pkt, cnt, numb_pkt,
                drone.pkt_id, sim_time, None, None, None)
            self.data_analizer.write_data_rx_pkt(tuple_test)
            print('none pkt can be inserted, the queue is full!')
        else:
            type_pkt = 'json'
            size_pkt = self.size_json
            priority_of_pkt = 1
            cnt = 1
            numb_pkt = 1
            UAV_sender.queue.put(
                (sim_time, queue_owner, drone.id, type_pkt, size_pkt,
                 priority_of_pkt, cnt, numb_pkt, drone.pkt_id))
            print('Drone: ', UAV_sender.id, 'json P1 pkt is inserted and the queue length is: ', UAV_sender.queue.qsize())
            drone.pkt_id += 1

        if flag_queue_empty:
            print('Drone: ', UAV_sender.id, 'there is no pkt in the queue excepted me, length: ', UAV_sender.queue.qsize() )
            self.channel_communication(UAV_sender, UAV_no_tx, sim_time)

    def check_bitRate_tx(self, UAV, relay, sim_time):
        #if when was inserted the pkt the UAV had bitrate non null, and at
        #the new attempt tx is null -> send the pkt at the relay
        while not UAV.queue.empty():
            tmp = UAV.queue.get()
            (gen_time, queue_owner, pkt_owner, pkt_type, size_pkt, priority_pkt, cnt_packet_sent, total_pkt, pkt_id) = tmp
            if priority_pkt == 1:
                self.check_queue(UAV, None, sim_time)

            if not relay.queue.full():
                relay.queue.get(tmp)
                if relay.queue.qsize() == 1:
                    self.channel_communication(relay, UAV, sim_time)
            else:
                state = 'removed congested queue'
                # updating metrics for the test&validation
                UAV.pkt_lost_tot += 1
                if pkt_type == 'json':
                    UAV.pkt_lost_json += 1
                else:
                    UAV.pkt_lost_jpg += 1
                UAV.pkt_lost_queue_full += 1

                tuple_test = (
                    sim_time, state, queue_owner, pkt_owner, pkt_type, size_pkt, priority_pkt, cnt_packet_sent, total_pkt,
                    pkt_id, gen_time, None, None, None)
                self.data_analizer.write_data_rx_pkt(tuple_test)

    def check_queue(self, UAV_sender, UAV_no_tx, sim_time):
        #pkt with high priority have to be stored -> check is queue is full -> remove 1 low p pkt if json,
        # remove multiple pkts if the type is jpg and belong to the same queue
        if UAV_sender.queue.full():
            self.remove_low_priority_pkts(UAV_sender, UAV_no_tx, sim_time)

    def remove_low_priority_pkts(self, UAV_sender, UAV_no_tx, sim_time):
        #a new temporary priority queue is created in order to don't lose the high priority packets
        tmp_queue = queue.PriorityQueue()

        #counter used for the counting jpg pkt
        cnt_pkt = 0
        cnt_tot_pkt = 0

        #counter index pkt in the queue
        index_pkt = 0
        #initialization of
        last_pkt_owner = -1
        #length of the full queue
        length_queue = UAV_sender.queue.qsize()

        #looking for the first low priority pkt
        while not UAV_sender.queue.empty():
            tupla = UAV_sender.queue.get()
            (generation_pkt_time, queue_owner, pkt_owner, type_pkt, size_pkt,
            priority_of_pkt, cnt, numb_pkt, pkt_id)= tupla
            if priority_of_pkt == 1:
                tmp_queue.put(tupla)
                index_pkt += 1
                print('0. Drone: ', UAV_sender.id, 'first pkt is a json P1')
            else:
                state = 'removed congested queue'

                #update the values for estimate if some pkts of the image have been sent yet -> so receiving image is corrupted
                cnt_pkt += 1
                cnt_tot_pkt = numb_pkt

                #if it is a json low priority pkt then the loop is broken
                if type_pkt == 'json':
                    # updating metrics for the test&validation
                    UAV_sender.pkt_lost_tot += 1
                    UAV_sender.pkt_lost_json += 1
                    UAV_sender.pkt_lost_queue_full += 1
                    if UAV_no_tx is not None:
                        UAV_no_tx.pkt_lost_tot += 1
                        UAV_no_tx.pkt_lost_json += 1
                        UAV_no_tx.pkt_lost_queue_full += 1

                    self.tot_pkt_lost += size_pkt
                    self.pkt_lost_interval_time += size_pkt
                    tuple_test = (
                        sim_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt, numb_pkt,
                        pkt_id, generation_pkt_time, None, None, None)
                    self.data_analizer.write_data_rx_pkt(tuple_test)
                    print('0. Drone: ', UAV_sender.id, 'pkt is ', type_pkt, 'pkt owner: ', pkt_owner, ' and the queue size: ', UAV_sender.queue.qsize())
                    break
                elif type_pkt == 'jpg':
                    #if im the new pkt is created by another drone,
                    # then the loop is broken and the packet is inserted already in the queue
                    if last_pkt_owner != pkt_owner and last_pkt_owner != -1:
                        print('2. Drone: ', UAV_sender.id, 'pkt is ', type_pkt, 'pkt owner: ', pkt_owner, 'and is regarding another file\n')
                        tmp_queue.put(tupla)
                        break
                    else:
                        # updating metrics for the test&validation
                        UAV_sender.pkt_lost_tot += 1
                        UAV_sender.pkt_lost_jpg += 1
                        UAV_sender.pkt_lost_queue_full += 1
                        if UAV_no_tx is not None:
                            UAV_no_tx.pkt_lost_tot += 1
                            UAV_no_tx.pkt_lost_json += 1
                            UAV_no_tx.pkt_lost_queue_full += 1
                        self.tot_pkt_lost += size_pkt
                        self.pkt_lost_interval_time += size_pkt
                        tuple_test = (
                            sim_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt, numb_pkt,
                            pkt_id, generation_pkt_time, None, None)
                        print('0. Drone: ', UAV_sender.id, 'pkt is ', type_pkt, 'pkt owner: ', pkt_owner, ' and the queue size: ', UAV_sender.queue.qsize())
                        #self.write_data_rx_pkt(tuple_test)
                        last_pkt_owner = pkt_owner
                        continue
                else:
                    print('Error in the digit type pkt\n')

                #if the frst pkt have to be removed -> then also the event related on the transmission is removed
                if index_pkt == 0:
                    self.cnt_iteration_per_each_UAV[UAV_sender] = 0
                    self.FES.remove_events( UAV_sender.id, 'Transmission attempt')
                    if not UAV_sender.queue.empty:
                        self.FES.add_events(sim_time, 'Transmission attempt', UAV_sender.id,)
                    print('3. Drone: ', UAV_sender.id, 'the pkt removed is the first one in the queue \n')

        #reintegration of pkts temporarily removed
        while not tmp_queue.empty():
            tupla = tmp_queue.get()
            UAV_sender.queue.put(tupla)

        if length_queue == index_pkt:
            print('None pkt has been removed, new pkts cannot be added')

        if cnt_tot_pkt != cnt_pkt:
            print ('The image that BS was receiving has been corrupted\n')

    def channel_communication(self, UAV_sender, UAV_no_tx, sim_time):

        #take the pkts from the queue
        tmp = UAV_sender.queue.get()
        (gen_time, queue_owner, pkt_owner, type_pkt, size_pkt,
        priority_of_pkt, cnt_packet_sent, total_pkt, pkt_id ) = tmp
        print ('00. Drone and pkt type: ', UAV_sender.id, type_pkt)
        # check the channel
        if self.state_channel == 'idle':
            print('1C. Drone: ', UAV_sender.id, 'the channel is IDLE \n')
            self.state_channel = 'busy'
            self.time_channel_is_getting_busy = sim_time

            # computation of the interval of time at which the channel is idle
            if self.time_channel_is_idle > 0:
                state = 'time channel idle'
                time_interval = self.time_channel_is_getting_busy - self.time_channel_is_idle
                tuple_test = (None, state, None, None, None, None, None, None, None, None, None, None, time_interval, None)
                self.data_analizer.write_data_rx_pkt(tuple_test)

            # computation of the tx time
            if UAV_sender.id == 0:
                tx_time = size_pkt / UAV_sender.drone.bitrate
            else:
                tx_time = size_pkt / UAV_sender.bitrate
            print('2C. Drone: ', UAV_sender.id, 'the tx_time is: ', tx_time,' \n')
            # prepare the event: Received data
            state = 'RECEIVED'
            identification = (
            gen_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
            total_pkt, pkt_id)
            self.FES.add_events (sim_time + tx_time, 'Received Data', identification )

            # remove the counter of the repetition of tx
            self.cnt_iteration_per_each_UAV[UAV_sender.id] = 0

            # scheduling another transmission of pkt belonging to the same UAV
            if not UAV_sender.queue.empty() and type_pkt == 'jpg':
                # if there are other pkts composing the image or json -> coordinate of the missing,
                # then the scheduling of the new event has a lower interval of time
                propagation_time = UAV_sender.distance_GS / 3e8
                self.FES.add_events(sim_time + tx_time + propagation_time/1e4, 'Transmission attempt', UAV_sender.id)
                print('3C. Drone and type pkt: ', UAV_sender.id, type_pkt, 'the queue is not empty -> jpg + json rescue file \n schedule the new transmission \n')

            # if instead there are other pkts in the UAV's queue but aren't correlated,
            # then the scheduling have an higher interal of time
            elif not UAV_sender.queue.empty() and type_pkt == 'json':
                tmp = UAV_sender.queue.get()
                (gen_time, queue_owner, pkt_owner, type_pkt, size_pkt,
                 priority_of_pkt, cnt_packet_sent, total_pkt, pkt_id) = tmp
                UAV_sender.queue.put(tmp)
                print('3C. Drone: ', UAV_sender.id,
                      'the queue is not empty ->  json telemetry file \n schedule the new transmission \n')
                # schedule the new pkt generating a rando wait (defined into the channel busy function)
                rnd_wait = (random.uniform(0, self.size_pkt / 50e5))
                self.FES.add_events(sim_time + tx_time + rnd_wait, 'Transmission attempt', UAV_sender.id)

        elif self.state_channel == 'busy':
            UAV_sender.queue.put(tmp)
            print('1CB. Drone: ', UAV_sender.id, 'the channel is BUSY and the queue size is: ', UAV_sender.queue.qsize(), '\n')
            self.channel_busy(UAV_sender, UAV_no_tx, priority_of_pkt, sim_time)

        else:
             print("ERROR: channel is neither busy nor idle")

    def channel_busy(self, UAV_sender, UAV_no_tx, priority_of_pkt, sim_time):
        self.cnt_iteration_per_each_UAV[UAV_sender.id] += 1
        print('2CB. Drone: ', UAV_sender.id, 'cnt_iteration attempts: ', self.cnt_iteration_per_each_UAV[UAV_sender.id], '\n')
        #remove pkt cnt expired
        if self.cnt_iteration_per_each_UAV[UAV_sender.id] > self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0 and priority_of_pkt == 0:
            print('3CB. Drone: ', UAV_sender.id, 'cnt_iteration attempts: ',
                  self.cnt_iteration_per_each_UAV[UAV_sender.id], ' -> expired counter -> remove pkt P0\n')
            self.remove_pkts_expired_tx(UAV_sender, UAV_no_tx, sim_time)
        #cnt not expired schedule the new transmission unless there are already other pkts in the qqueue
        elif self.cnt_iteration_per_each_UAV[UAV_sender.id] <= self.MAX_NUMB_OF_ATTEMPTIONS_TX_p0 and priority_of_pkt == 0:
            rnd_wait = (
                random.uniform(0, (self.size_pkt / 50e5) * 2 ** (self.cnt_iteration_per_each_UAV[UAV_sender.id] - 1)))
            if isinstance(rnd_wait, np.ndarray):
                rnd_wait = rnd_wait.item()
            self.FES.add_events(sim_time + rnd_wait, 'Transmission attempt', UAV_sender.id)
            print('2CB. Drone: ', UAV_sender.id, ' piority: ', priority_of_pkt,'cnt_iteration attempts: ',
                  self.cnt_iteration_per_each_UAV[UAV_sender.id],
                    ' and reattempt tx : ', rnd_wait, '\n')

        elif self.cnt_iteration_per_each_UAV[UAV_sender.id] > self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1 and priority_of_pkt == 1:
            print('3CB. Drone: ', UAV_sender.id, 'cnt_iteration attempts: ',
                  self.cnt_iteration_per_each_UAV[UAV_sender.id], ' -> expired counter -> remove pkt P1\n')
            self.remove_pkts_expired_tx(UAV_sender, UAV_no_tx, sim_time)

        elif self.cnt_iteration_per_each_UAV[UAV_sender.id] <= self.MAX_NUMB_OF_ATTEMPTIONS_TX_p1 and priority_of_pkt == 1:
            rnd_wait = (random.uniform(0, self.size_pkt / 20e5))
            if isinstance(rnd_wait, np.ndarray):
                rnd_wait = rnd_wait.item()
            self.FES.add_events(sim_time + rnd_wait, 'Transmission attempt', UAV_sender.id)
            print('2CB. Drone: ', UAV_sender.id, ' piority: ', priority_of_pkt, 'cnt_iteration attempts: ',
                  self.cnt_iteration_per_each_UAV[UAV_sender.id],
                ' and reattempt tx : ', rnd_wait, '\n')

    def remove_pkts_expired_tx(self, UAV_sender, UAV_no_tx, sim_time):
        # experied attempts tx -> remove pkt
        tmp = UAV_sender.queue.get()
        (gen_time, queue_owner, pkt_owner, pkt_type, size_pkt,
         priority_pkt, cnt_packet_sent, total_pkt, pkt_id) = tmp
        print('4CB. Drone: ', UAV_sender.id, '-> expired counter -> remove pkt: ', pkt_type, ' priority pkt: ',priority_pkt, '\n')
        state = 'removed tx attempts expired'
        tuple_test = (
            sim_time, state, queue_owner, pkt_owner, pkt_type, size_pkt, priority_pkt, cnt_packet_sent, total_pkt,
            pkt_id, gen_time, None, None, None)
        self.data_analizer.write_data_rx_pkt # is used for the test and validation

        self.cnt_iteration_per_each_UAV[UAV_sender.id] = 0
        self.data_analizer.write_data_rx_pkt(tuple_test)
        UAV_sender.pkt_lost_tot += 1
        if pkt_type == 'json':
            UAV_sender.pkt_lost_json += 1
        else:
            UAV_sender.pkt_lost_jpg += 1
        UAV_sender.pkt_lost_iteration += 1

        if UAV_no_tx is not None:
            UAV_no_tx.pkt_lost_tot += 1
            if pkt_type == 'json':
                UAV_no_tx.pkt_lost_json += 1
            else:
                UAV_no_tx.pkt_lost_jpg += 1
            UAV_no_tx.pkt_lost_iteration += 1

        self.tot_pkt_lost += size_pkt
        self.pkt_lost_interval_time += size_pkt

        # if the queue is not empty -> then schedule the transmission of the other pkt
        if not UAV_sender.queue.empty():
            self.FES.add_events(sim_time, 'Transmission attempt', UAV_sender.id)
            print('5CB. Drone: ', UAV_sender.id, '-> pkt removed but the queue is not emptry -> schedule a new tx\n')

    def received_data(self, identification, UAV_tx, sim_time):
        (gen_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
        total_pkt, pkt_id) = identification


        if type_pkt == 'jpg':
            UAV_tx.pkt_cnt_jpg += 1
            if UAV_tx.pkt_cnt_jpg < total_pkt:
                if UAV_tx.pkt_cnt_jpg == 0:
                    UAV_tx.start_tx_jpg = gen_time
                print('\n pkt cnt_jpg = ', UAV_tx.pkt_cnt_jpg, 'total pkt: ', total_pkt )
                UAV_tx.total_latency_jpg = None
            else:
                UAV_tx.pkt_cnt_jpg = 0
                UAV_tx.total_latency_jpg = -1
             #   print('\n cnt_jpg = ', UAV_tx.pkt_cnt_jpg,
              #        'its intializated and the latency of jpg is =  ', UAV_tx.total_latency_jpg)
        else:
            UAV_tx.total_latency_jpg = sim_time - gen_time
          #  print('\n cnt_jpg = ', UAV_tx.pkt_cnt_jpg,
           #       'its intializated and the latency of json is = ', UAV_tx.total_latency_jpg)

        tuple_test = (
            sim_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
            total_pkt, pkt_id, gen_time, sim_time, None, UAV_tx.total_latency_jpg)
        self.data_analizer.write_data_rx_pkt(tuple_test)

        self.gs.buffer.put((sim_time, gen_time, queue_owner, pkt_owner, priority_of_pkt, type_pkt, cnt_packet_sent, total_pkt ))
        self.gs.receive()

        self.state_channel = 'idle'