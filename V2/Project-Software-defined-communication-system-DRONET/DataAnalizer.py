# Copyright 2023 Cuzzi Andrea
#           2023 Logruosso Loredana
#           2023 Nepote Luca
#
# This file is part of DronetSim.
#
# DronetSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
#
# DronetSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DronetSim. If not, see <http://www.gnu.org/licenses/gpl-2.0.html>.
#
# The authors and contributors are listed in the following line:
# Cuzzi Andrea, Logruosso Loredana, Nepote Luca

FLAG_OS = 'Windows'
if FLAG_OS == 'MAC':
    import matplotlib
    matplotlib.use('Qt5Agg')  # importa il backend Qt5Agg #su windows bisogna commentarlo

import csv
import os.path
import numpy as np
import pandas as pd

from scipy.stats import norm, t

class data_analizer:

    def __init__(self, FES, delta_t_msg):
        self.pkt_lost_tot_interval_time = 0
        self.past_time_throughp = 0
        self.pkt_lost_expired_interval_time = 0
        self.pkt_lost_expired_int_time_UAVs = 0
        self.pkt_lost_expired_int_time_relay = 0
        self.pkt_lost_congested_interval_time = 0
        self.pkt_lost_congested_int_time_UAVs = 0
        self.pkt_lost_congested_int_time_relay = 0
        self.pkt_lost_int_time_relay = 0
        self.pkt_lost_int_time_UAVs = 0
        self.numb_bit_rx_in_dt = 0
        self.numb_tot_bit_rx = 0
        self.numb_relay_bit_rx = 0
        self.numb_uav_bit_rx = 0
        self.numb_bit_generated_in_dt = 0
        self.numb_bit_rx_UAVs = 0
        self.numb_bit_rx_relay = 0
        self.latency_summation = 0
        self.latency_sum_UAVs = 0
        self.latency_sum_relay = 0
        self.numb_tot_bit_generated = 0
        self.n_pkt_received = 0
        self.n_pkt_received_relay = 0
        self.n_pkt_received_uav = 0
        self.n_tot_pkt_generated = 0
        self.n_pkt_generated_in_dt = 0
        self.compute_throughput = 0

        self.THROUGHPUT_tot = None
        self.THROUGHPUT_relay = None
        self.THROUGHPUT_UAVs = None
        self.latency_relay = None
        self.latency_UAVs = None
        self.lost_pkt_tot_bps = None
        self.lost_pkt_relay = None
        self.lost_pkt_UAVs = None

        self.delta_t_msg = delta_t_msg

        self.FES = FES

        #check file cvs
        # Check if the file exists
        self.file_exists1 = os.path.isfile('data_throughput.csv')
        if self.file_exists1:
            os.remove('data_throughput.csv')
            self.file_exists1 = False

        self.file_exists2 = os.path.isfile('data_bitloss.csv')
        if self.file_exists2:
            os.remove('data_bitloss.csv')
            self.file_exists2 = False

        self.file_exists3 = os.path.isfile('data_latency.csv')
        if self.file_exists3:
            os.remove('data_latency.csv')
            self.file_exists3 = False

    def flag_compute_throughput(self, compute_throughput):
        self.compute_throughput = compute_throughput

    def write_data_rx_pkt(self, identification):
        ( sim_time, state, queue_owner, pkt_owner, pkt_type, size_pkt, priority_of_pkt, cnt_packet_sent, total_pkt,
            pkt_id, time_generated, received_time, interval_time_ch_idle, latency_pkts, delta_msg_varying) = identification
        total_load = None

    #    print('\n\ndelta_msg_varying: ', delta_msg_varying, '\n\n')
        if state == 'RECEIVED':
          #  print('DATA ANALIZER ive recive the  pkt:', identification)
            latency = received_time - time_generated

            # total number of bits received in the interval of time for the throughput computation
            self.numb_bit_rx_in_dt += size_pkt
            # total number of bits received
            self.numb_tot_bit_rx += size_pkt
            # total number of bits generated in the interval of time for the throughput computation
            self.numb_bit_generated_in_dt += size_pkt
            # total number of bits generated
            self.numb_tot_bit_generated += size_pkt

            #used for the comoutation of the latency of the whole file, i.e the whole jpg or json
            if latency_pkts == -1:
                total_lat = latency
            else:
                total_lat = latency_pkts

            if total_lat is not None:  # Verifica se total_lat è un valore numerico valido
                self.latency_summation += total_lat#somma le latenze che poi verrano mediate
                if queue_owner == 'relay':
                    self.latency_sum_relay += total_lat
                else:
                    self.latency_sum_UAVs += total_lat

            total_load = self.numb_tot_bit_generated / sim_time

            if queue_owner == 'relay':
                # number of bits received from relay
                self.numb_bit_rx_relay += size_pkt
                self.numb_relay_bit_rx += size_pkt
                self.n_pkt_received_relay += 1
            else:
                # number of bits received from 'normal' drones
                self.numb_bit_rx_UAVs += size_pkt
                self.numb_uav_bit_rx += size_pkt
                self.n_pkt_received_uav += 1

            #generally computed the number od received pkts
            self.n_pkt_received += 1
            self.n_tot_pkt_generated += 1
            self.n_pkt_generated_in_dt += 1

            # latency
            latency_tot = self.latency_summation / self.n_pkt_received
          #average the latency in function of the number of the received pkts
            if self.n_pkt_received_relay > 0:
                self.latency_relay = self.latency_sum_relay / self.n_pkt_received_relay
            else:
                self.latency_relay = 0
            if self.n_pkt_received_uav > 0:
                self.latency_UAVs = self.latency_sum_UAVs / self.n_pkt_received_uav
            else:
                self.latency_UAVs = 0

            #compute the throughput
            self.THROUGHPUT_tot = self.numb_tot_bit_rx / sim_time
            self.THROUGHPUT_relay = self.numb_relay_bit_rx / sim_time
            self.THROUGHPUT_UAVs = self.numb_uav_bit_rx / sim_time

            # Write data to CSV file
            with open('data_throughput.csv', 'a', newline='') as file:
                writer = csv.writer(file)
            #write the whole parameters about the throughput in the file
                # Write header if the file is newly created
                if not self.file_exists1:
                    writer.writerow(
                        ['sim time[s]', 'generated time[s]', 'received time[s]', 'queue_owner', 'ID UAV', 'ID pkt',
                         'priority',
                         'type', 'size file[bit]', 'cnt packet_sent', 'total pkt', 'state', 'latency per pkt[s]',
                         'total latency [s]',
                         'throughput tot[bps]', 'throughput RELAY [bps]', 'throughput UAVs [bps]',
                         'total load [bps]', 'delta t msg',
                         'interval_time_ch_idle[s]'])
                    self.file_exists1 = True  # Update the flag after writing the header
                writer.writerow(
                    [sim_time, time_generated, received_time, queue_owner, pkt_owner, pkt_id, priority_of_pkt,
                     pkt_type, size_pkt, cnt_packet_sent, total_pkt, state, latency, total_lat,
                     self.THROUGHPUT_tot, self.THROUGHPUT_relay, self.THROUGHPUT_UAVs, total_load, delta_msg_varying,
                     interval_time_ch_idle])


            # Write data to CSV file
          # write the whole parameters about the latency in the file
            with open('data_latency.csv', 'a', newline='') as file:
                writer = csv.writer(file)

                # Write header if the file is newly created
                if not self.file_exists3:
                    writer.writerow(
                        ['sim time[s]', 'generated time[s]', 'received time[s]', 'queue_owner', 'ID UAV', 'ID pkt',
                         'priority',
                         'type', 'size file[bit]', 'cnt packet_sent', 'total pkt', 'state', 'latency per pkt[s]',
                         'total latency [s]',
                         'latency tot[bps]', 'latency RELAY [bps]', 'latency UAVs [bps]', 'delta msg [s]'
                         ])
                    self.file_exists3 = True  # Update the flag after writing the header

                writer.writerow(
                    [sim_time, time_generated, received_time, queue_owner, pkt_owner, pkt_id, priority_of_pkt,
                     pkt_type, size_pkt, cnt_packet_sent, total_pkt, state, latency, total_lat,
                     latency_tot, self.latency_relay, self.latency_UAVs, delta_msg_varying
                     ])
            #   print('DATA ANALIZER 2 sono stati trascritti su csv simtime: ', sim_time)
        # compute the bit lost given a specific state indicating the reason why the pkt is removed
        #so first sum up all the bit of the pkts that have been losot and then average it over the simulation time
        elif state == 'removed - congestion':
            # total number of bits generated
            self.numb_tot_bit_generated += size_pkt
            self.numb_bit_generated_in_dt += size_pkt
            self.n_tot_pkt_generated += 1
            self.n_pkt_generated_in_dt += 1

            total_load = self.numb_tot_bit_generated / sim_time

            if queue_owner == 'relay':
                self.pkt_lost_congested_int_time_relay += size_pkt
                self.pkt_lost_int_time_relay += size_pkt
            else:
                self.pkt_lost_congested_int_time_UAVs += size_pkt
                self.pkt_lost_int_time_UAVs += size_pkt

            self.pkt_lost_congested_interval_time += size_pkt
            self.pkt_lost_tot_interval_time += size_pkt

        elif state == 'removed - expiration':
            # total number of bits generated
            self.numb_tot_bit_generated += size_pkt
            self.numb_bit_generated_in_dt += size_pkt
            self.n_tot_pkt_generated += 1
            self.n_pkt_generated_in_dt += 1

            total_load = self.numb_tot_bit_generated / sim_time

            if queue_owner == 'relay':
                self.pkt_lost_expired_int_time_relay += size_pkt
                self.pkt_lost_int_time_relay += size_pkt
            else:
                self.pkt_lost_expired_int_time_UAVs += size_pkt
                self.pkt_lost_int_time_UAVs += size_pkt

            self.pkt_lost_expired_interval_time += size_pkt
            self.pkt_lost_tot_interval_time += size_pkt


        if state == 'removed - congestion' or 'removed - expiration':
            lost_pkt_congested_bps_relay = self.pkt_lost_congested_int_time_relay / sim_time
            lost_pkt_congested_bps_UAVs = self.pkt_lost_congested_int_time_UAVs / sim_time
            lost_pkt_congested_bps = self.pkt_lost_congested_interval_time / sim_time

            lost_pkt_expired_bps_relay = self.pkt_lost_expired_int_time_relay / sim_time
            lost_pkt_expired_bps_UAVs = self.pkt_lost_expired_int_time_UAVs / sim_time
            lost_pkt_expired_bps = self.pkt_lost_expired_interval_time / sim_time

            self.lost_pkt_UAVs = self.pkt_lost_int_time_UAVs / sim_time
            self.lost_pkt_relay = self.pkt_lost_int_time_relay / sim_time
            self.lost_pkt_tot_bps = self.pkt_lost_tot_interval_time / sim_time

            with open('data_bitloss.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                # Write header if the file is newly created
                #write the whole parameters about the bit loos in the file
                if not self.file_exists2:
                    writer.writerow(
                        ['sim time[s]', 'generated time[s]', 'received time[s]', 'queue_owner', 'ID UAV', 'ID pkt',
                         'priority', 'type', 'size file[bit]', 'cnt packet_sent', 'total pkt', 'state',
                         'total load [bps]',
                         'bit tot lost[bps]', 'bit relay lost[bps]', 'bit UAVs lost[bps]',
                         'bit lost congestion[bps]', 'bit cong relay lost[bps]', 'bit cong UAVs lost',
                         'bit lost expired[bps]', 'bit exp relay lost[bps]', 'bit exp UAVs lost', 'delta_t_msg']
                    )
                    self.file_exists2 = True  # Update the flag after writing the header
                writer.writerow(
                    [sim_time, time_generated, received_time, queue_owner, pkt_owner, pkt_id, priority_of_pkt,
                     pkt_type, size_pkt, cnt_packet_sent, total_pkt, state, total_load,
                     self.lost_pkt_tot_bps, self.lost_pkt_relay, self.lost_pkt_UAVs,
                     lost_pkt_congested_bps, lost_pkt_congested_bps_relay, lost_pkt_congested_bps_UAVs,
                     lost_pkt_expired_bps, lost_pkt_expired_bps_relay, lost_pkt_expired_bps_UAVs, delta_msg_varying]
                )

