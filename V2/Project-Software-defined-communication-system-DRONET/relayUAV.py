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
        self.pkt_lost_iteration = 0  # pacchetti persi dovuti al numero di tentativi di ritrasmissione
        self.pkt_lost_json = 0  # pacchetti vecchi non ancora inviati
        self.pkt_lost_jpg = 0  # pacchetti jpg persi dovuti al nuovo pkt
        self.pkt_cnt_jpg = 0 #needed for counting the number of received pkts of an image
        self.pkt_lost_P1 = 0 #pkt P1 lost due to their congested queue
        self.total_latency_jpg = 0 #needed for the comupation of the image latency
        self.start_tx_jpg = 0 #latency compuatation starting time
        self.queue = queue.PriorityQueue(maxsize = max_length_queue)
        self.flag_start_TX = False
        self.channel_relay = 'idle'

        self.radious_relay = 290

        #bitrate between relay and UAV with null bitrate
        self.bitrate_UAV_rel = self.drone.bitRate_max

    def veloc_real(self, wind_speed, wind_angle, x_new, y_new):
        # mountain position
        self.drone.x_new = x_new
        self.drone.y_new = y_new

        delta_x_new = (self.drone.x_new - self.drone.x)
        delta_y_new = (self.drone.y_new - self.drone.y)
        # angle towards the mountain
        self.drone.teta = math.atan2(delta_y_new, delta_x_new)  # angolo tra il nuovo segmento e l'orizzontale

        self.drone.velocity_real(wind_speed, wind_angle)

    def reach_top_mountain(self, time_interval):

        self.drone.cnt_iteration(time_interval)
        if self.drone.tot_iterazioni > 0:

            if time_interval > 0: # could happen that the time interval is equal to 0
                # move the drone #
                self.drone.move(time_interval)
                # compute the needed iterations to reach the generated waypoint
                self.drone.cnt_iteration(time_interval)

            # update the number of iteration #
            self.drone.tot_iterazioni -= 1

        dist_RELAY_MOUNT = ((self.drone.x - self.drone.x_new) ** 2 + (self.drone.y - self.drone.y_new) ** 2) ** 0.5
        self.distance_GS = dist_RELAY_MOUNT

        if dist_RELAY_MOUNT < 9 and not self.FLAG_ARRIVED:
            self.FLAG_ARRIVED = True
            for j in range(1, self.N_UAV + 1):
                # self.FES.put((self.DELTA_t_MSG_TO_SENT + (rnd_initial_time[j - 1]), "Send Telemetry Data", j))
                self.FES.add_events(self.DELTA_t_MSG_TO_SENT, "Send Telemetry Data", j)

    def bitrate_relay_UAV(self, coord_UAV_x, coord_UAV_y, Mountain_pos):

        coord_UAV_x = coord_UAV_x * self.SF
        coord_UAV_y = coord_UAV_y * self.SF

        # update bitrate based on distance from gs
        self.distance_relay_UAV = math.sqrt((coord_UAV_x - Mountain_pos[0]) ** 2 + (coord_UAV_y - Mountain_pos[1]) ** 2)
        # print('UAV-GS: distance: ', self.distance_GS, 'coord: (', coord_x, ', ', coord_y, ')')

        m = -self.bitRate_max / (2.5e3 - 2e3)

        if self.distance_relay_UAV < 2e3:
            self.bitrate_UAV_rel = self.bitRate_max

        elif 2e3 <= self.distance_relay_UAV < 2.5e3:
            self.bitrate_UAV_rel = m * (self.distance_relay_UAV - 2e3) + self.bitRate_max  # con equazione della retta

        else:
            self.bitrate_UAV_rel = 0

