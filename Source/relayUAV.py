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


import math
import random
import numpy as np
import queue
from Drone import Drone

class Relay:
    def __init__(self, gs, T_lim, T_in, V_in, I_in, E, add_cons, Ej, mod_v_real, max_length_queue, SCALE_FACTOR, N_miss, N_UAV, FES, DELTA_t_MSG_TO_SENT):
        self.FLAG_ARRIVED = False
        self.DELTA_t_MSG_TO_SENT = DELTA_t_MSG_TO_SENT
        self.teta = 0
        self.id = 0
        self.N_UAV = N_UAV
        self.FES = FES
        self.SF = SCALE_FACTOR
        self.drone = Drone(self.id, gs, T_lim, T_in, V_in, I_in, E, add_cons, Ej, mod_v_real, max_length_queue, N_miss)
        self.bitRate_max = self.drone.bitRate_max

        self.bitrate = self.bitRate_max
        self.pkt_lost_tot = 0
        self.pkt_lost_queue_full = 0
        # lost packets due to number of retransmission attempts
        self.pkt_lost_iteration = 0
        # old packages not yet sent
        self.pkt_lost_json = 0
        # jpg packets lost due to the new pkt
        self.pkt_lost_jpg = 0
        # needed for counting the number of received pkts of an image
        self.pkt_cnt_jpg = 0
        # pkt P1 lost due to their congested queue
        self.pkt_lost_P1 = 0
        # needed for the computation of the image latency
        self.total_latency_jpg = 0
        # latency computation starting time
        self.start_tx_jpg = 0
        self.queue = queue.PriorityQueue(maxsize = max_length_queue)
        self.flag_start_TX = False
        self.channel_relay = 'idle'

        #bitrate between relay and UAV with null bitrate
        self.bitrate_UAV_rel = self.drone.bitRate_max

    def veloc_real(self, wind_speed, wind_angle, x_new, y_new):
        # mountain position
        self.drone.x_new = x_new
        self.drone.y_new = y_new

        delta_x_new = (self.drone.x_new - self.drone.x)
        delta_y_new = (self.drone.y_new - self.drone.y)

        # angle towards the mountain
        self.drone.teta = math.atan2(delta_y_new, delta_x_new)

        self.drone.velocity_real(wind_speed, wind_angle)

    def reach_top_mountain(self, time_interval):

        self.drone.cnt_iteration(time_interval)

        if self.drone.tot_iterazioni > 0:
            # could happen that the time interval is equal to 0
            if time_interval > 0:
                # move the drone #
                self.drone.move(time_interval)
                # compute the needed iterations to reach the generated waypoint
                self.drone.cnt_iteration(time_interval)

            # update the number of iteration #
            self.drone.tot_iterazioni -= 1

        # distance between the relay and the top of the mountain
        dist_RELAY_MOUNT = ((self.drone.x - self.drone.x_new) ** 2 + (self.drone.y - self.drone.y_new) ** 2) ** 0.5
        self.distance_GS = dist_RELAY_MOUNT

        if dist_RELAY_MOUNT < 9 and not self.FLAG_ARRIVED:
            self.FLAG_ARRIVED = True

    def bitrate_relay_UAV(self, coord_UAV_x, coord_UAV_y, Mountain_pos):

        # coordinates of UAV transmitting to relay
        coord_UAV_x = coord_UAV_x * self.SF
        coord_UAV_y = coord_UAV_y * self.SF

        # update bitrate based on distance from gs
        self.distance_relay_UAV = math.sqrt((coord_UAV_x - Mountain_pos[0]) ** 2 + (coord_UAV_y - Mountain_pos[1]) ** 2)

        # slope
        m = -self.bitRate_max / (2.5e3 - 2e3)

        if self.distance_relay_UAV < 2e3:
            self.bitrate_UAV_rel = self.bitRate_max

        elif 2e3 <= self.distance_relay_UAV < 2.5e3:
            self.bitrate_UAV_rel = m * (self.distance_relay_UAV - 2e3) + self.bitRate_max  # con equazione della retta

        else:
            self.bitrate_UAV_rel = 0

