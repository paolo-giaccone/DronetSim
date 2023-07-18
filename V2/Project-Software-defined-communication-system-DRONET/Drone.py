import math
import random
import numpy as np
import queue

class Drone:
    def __init__(self, id, gs, T_lim, T_in, V_in, I_in, E, add_cons, Ej, mod_v_real, max_length_queue, N_missings):
        self.x_new = 0
        self.y_new = 0
        self.gs = gs
        self.x = self.gs.x  # starting position same as the gs
        self.y = self.gs.y
        self.tot_iterazioni = 0
        self.mod_v_app = 13  # meters per second
        self.mod_v_real = mod_v_real
        self.ang_v_app = 0
        self.teta = 0
        self.distance = 0
        self.bitRate_max = 1e5 # bps
        self.bitrate = self.bitRate_max  # initial
        self.bitrate_Relay_UAV = self.bitRate_max  # initial
        self.End_points = []
        self.velocity = []
        self.coeff = 1
        self.found_missing_flag = np.zeros((N_missings, 1)) #whene the drone has discovered the missing then it sends just once the coordinates to the BS
        self.how_many_missing_are_found = np.zeros((N_missings, 1))
        self.time_past = 0

        self.T_lim = T_lim
        self.T_in = T_in  # initial temperature
        self.V_in = V_in  # [V]
        self.I_in = I_in  # [A]
        self.P = V_in * I_in #[W]
        self.E = E  # [Wh] initial energy
        self.Time_aut = self.P / self.E * 60  # tempo di autonomia del drone [min]
        self.add_cons = add_cons  # additional power consumption of the battery
        self.Ej = Ej  # initial battery energy in joule [J]
        self.Ej_check = Ej
        self.deltaT = 0

        self.id = id
        # at Starting point there is no power consumption
        self.act_cons = 0
        self.distance_GS = 0
        self.FLAG_PC = True
        GREEN = (0, 255, 0, 200)
        self.circle_color = GREEN

        # Available energy
        self.check_f = 0

        self.alpha1 = 0
        self.alpha2 = 0
        self.alpha_drone = 0
        self.FLAG_Interrupt = True # the drone has battery level different from 0

        #communication
        self.queue = None
        self.size_jpg = 0
        self.queue = queue.PriorityQueue(maxsize=max_length_queue)
        self.pkt_lost_tot = 0
        self.pkt_lost_queue_full = 0
        self.pkt_lost_iteration = 0  # pacchetti persi dovuti al numero di tentativi di ritrasmissione
        self.pkt_lost_json = 0  # pacchetti vecchi non ancora inviati
        self.pkt_lost_jpg = 0  # pacchetti jpg persi dovuti al nuovo pkt
        self.pkt_id = 0
        self.pkt_lost_P1 = 0
        self.pkt_cnt_jpg = 0
        self.start_tx_jpg = 0
        self.total_latency_pkt = 0
        self.im_tx_to_RELAY = None  #variable used in the communication
        self.im_tx_to_GS = None #variable used in the communication


    # update effective velocity (mod_v_real) of the drone according to the wind
    def velocity_real(self, wind_mod, gamma):
        if wind_mod: #if different from 0
            a = math.cos(self.teta)**2 + math.sin(self.teta)**2
            b = -2*wind_mod*((math.cos(self.teta) * math.cos(gamma)) + (math.sin(self.teta) * math.sin(gamma)))
            c = wind_mod**2 * math.cos(gamma)**2 + wind_mod**2 * math.sin(gamma)**2 - self.mod_v_app**2

            x1 = (-b + (math.sqrt(b ** 2 - (4 * a * c)))) / (2 * a)
            x2 = (-b - (math.sqrt(b ** 2 - (4 * a * c)))) / (2 * a)
            if x1 >= 0:
                self.mod_v_real = x1
            else:
                self.mod_v_real = x2

             # angolo di A rispetto all'asse orizzontale
            cos_a_A = (wind_mod ** 2 + self.mod_v_app ** 2 - self.mod_v_real ** 2) / (2 * wind_mod * self.mod_v_app)
            ang_v_app = math.acos(cos_a_A)

            # verifichiamo il quadrante corretto per a_A
            v_app_x = self.mod_v_app * math.cos(ang_v_app)
            v_app_y = self.mod_v_app * math.sin(ang_v_app)
            ang_v_app = math.atan2(v_app_y, v_app_x)  # in senso orario
            self.ang_v_app = math.pi - ang_v_app
        else: # if wind speed is null
            self.mod_v_real=self.mod_v_app

    def power_consumption(self, sample_T, T_amb):

        # Costant UAV speed. The power is invariant to the wind but change with temperature
        # somma vettoriale per componenti, poi rapporto tra i moduli delle velocità per trovare il valore del coefficiente beta
        # gamma=angolo tra vento e orizzontale [0-360°]
        #v_ratio = self.mod_v_app / self.mod_v_real

        #if v_ratio >= 1:
         #   beta = v_ratio

        #elif v_ratio < 1:
          #  beta = 0.5 * v_ratio + 0.5
        eta=1
        alpha=1
        beta=1

        if T_amb in range(self.T_lim, 2*self.T_lim+1):  # +1 not included
            alpha = 1  # battery
            eta = 1 # moving
            self.deltaT = 1
        elif T_amb in range(0, self.T_lim) or T_amb > 2*self.T_lim:

            if self.FLAG_PC:
                # battery efficiency decrease by increasing the difference between the ideal temperature and the T_amb
                alpha = 1 - 1 / 3 * (abs(self.T_lim - T_amb) / self.T_lim)
                self.FLAG_PC = False
            else:
                alpha = 1

            # if the temperature is under 20° the power consumption is bigger
            eta = 1 + abs(self.T_lim - T_amb) * self.add_cons

        elif T_amb < 0:
            if self.FLAG_PC:
                # it is assumed that under 0°C the battery temperature remain constant
                alpha = 2 / 3
                self.FLAG_PC = False
            else:
                alpha = 1

            self.deltaT = 3

            eta = 1 + abs(self.T_lim - T_amb) * self.add_cons


        self.act_cons = eta * self.P * sample_T * beta  # actual consumption


        if not self.check_f:
            # updating of the battery energy every sample time
            self.Ej = alpha * self.Ej - self.act_cons
        else:
            # check if it is not negative
            self.Ej_check = alpha * self.Ej - self.act_cons

        self.Previous_T_amb = T_amb

     #   print("Actual consumption at time", sample_T, ":", self.act_cons/3600, "[Wh]")
     #   print("Actual energy available at time", sample_T, ":", self.Ej/3600, "[Wh]")

    def checkAvailabilityBattery(self, temperature, delta_T, Simulation):

        battery_level = self.Ej * 100 / Simulation.Initial_Ej

        deltaTemp_max = -1  # worst case, battery decreases quicker if the temperature decreases (max possible decraese in temperature)
        Temp_updated = temperature + deltaTemp_max

        # battery level below 20%
        if battery_level <= 20:
            self.check_f = 1
            self.power_consumption(delta_T, Temp_updated)
            battery_level_prov = self.Ej_check * 100 / Simulation.Initial_Ej
            if battery_level_prov < 0:
                self.FLAG_Interrupt = False  # return False to indicate loop should break
            else:
                # at the next Update UAV location event decrease the remaining battery level
                self.Ej_check = self.Ej
                self.check_f = 0
                self.FLAG_Interrupt = True

    # generate the next waypoint
    def trajectory_UAV(self, x_shift, y_shift, n_rows, n_cols, Waypoint, ARDUPILOT):
        if not ARDUPILOT:
            # set the specific subarea
            if self.id % n_cols == 0:
                i_x = n_cols
                i_y = self.id/n_cols

            elif self.id % n_cols != 0:
                i_x = self.id%n_cols
                i_y = np.ceil(self.id/n_cols)

            # relative position in the sub area
            self.x_new = random.uniform(0, 2*x_shift)
            self.y_new = random.uniform(0, 2*y_shift)

            # absolute position
            self.x_new += 2*x_shift*(i_x-1)
            self.y_new += 2*y_shift*(i_y-1)

        # ARDUPILOT Planning
        else:
            self.x_new = Waypoint[0]
            self.y_new = Waypoint[1]

        # distance from the next waypoint
        delta_x_new = (self.x_new - self.x)
        delta_y_new = (self.y_new - self.y)
        self.distance = math.sqrt(delta_x_new ** 2 + delta_y_new ** 2)

        # angle between the new direction and the horizontal
        self.teta = math.atan2(delta_y_new, delta_x_new)

        # save all the waypoint generated for each UAV
        self.End_points.append((self.x_new, self.y_new))

    # set the first waypoint at the center of the specific subarea
    def first_position(self, x_shift, y_shift, i_x, i_y):

        # center of the subarea
        self.x_new = 2*x_shift*(i_x-1) + x_shift
        self.y_new = 2*y_shift*(i_y-1) + y_shift

        delta_x_new = (self.x_new - self.x)
        delta_y_new = (self.y_new - self.y)
        self.distance = math.sqrt(delta_x_new ** 2 + delta_y_new ** 2)

        # angle between the new direction and the horizontal
        self.teta = math.atan2(delta_y_new, delta_x_new)

        # save all the waypoint generated for each UAV
        self.End_points.append((self.x_new, self.y_new))

    # compute the needed iteration to reach the waypoint
    def cnt_iteration(self, time_slot):
        distance = math.sqrt((self.x_new - self.x) ** 2 + (self.y_new - self.y) ** 2)
        time_to_reach = distance / self.mod_v_real

        if time_slot > 0:
            self.tot_iterazioni = np.round(time_to_reach / time_slot)

    #
    def move(self, time_slot):
        # simulated time
        delta_t = time_slot
        dx = self.mod_v_real*delta_t*math.cos(self.teta)
        dy = self.mod_v_real*delta_t*math.sin(self.teta)
        # move the drone based on its speed and the time delta
        self.x += dx
        self.y += dy
        # remaining distance to reach the waypoint
        self.distance = math.sqrt((self.x_new - self.x) ** 2 + (self.y_new - self.y) ** 2)

    def bitrate_fun(self, scale_factor):

        coord_x = self.x * scale_factor
        coord_y = self.y * scale_factor

        # update bitrate based on distance from gs
        self.distance_GS = math.sqrt((coord_x - self.gs.x) ** 2 + (coord_y - self.gs.y) ** 2)
        # print('UAV-GS: distance: ', self.distance_GS, 'coord: (', coord_x, ', ', coord_y, ')')

        m = -self.bitRate_max / (2.5e3 - 2e3)

        if self.distance_GS < 2e3:
            self.bitrate = self.bitRate_max

        elif 2e3 <= self.distance_GS < 2.5e3:
            self.bitrate = m * (self.distance_GS - 2e3) + self.bitRate_max  # con equazione della retta

        else:
            self.bitrate = 0

    def obstacle_fun(self, x_c, y_c, r, type_object, distance_obstacle_GS, scale_factor):

        x_c *= scale_factor
        y_c *= scale_factor
        r *= scale_factor

        pos_x = self.x*scale_factor
        pos_y = self.y*scale_factor

        a = (x_c - pos_x) ** 2 - r ** 2
        b = 2 * (x_c * pos_y - pos_x * pos_y - x_c * y_c + pos_x * y_c)
        c = (y_c - pos_y) ** 2 - r ** 2

        Delta = b ** 2 - 4 * a * c
        if Delta < 0:
            if type_object == 1:
                self.coeff = 1
            elif type_object == 2:
                self.coeff = 0.5

            #self.bitrate *= self.coeff
            return self.coeff

        if a != 0:
            m1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)  # slope
            m2 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)  # slope
        elif a == 0:
            m1 = math.pi/2
            m2 = math.pi/2

        if(pos_x < x_c - r) and (pos_y < y_c): # 1°
             self.alpha1 = math.atan(m1)
             self.alpha2 = math.atan(m2)
        elif (x_c - r < pos_x < x_c) and (pos_y < y_c): # 1°
             self.alpha1 = math.atan(m1) + math.pi
             self.alpha2 = math.atan(m2)
        elif (pos_x > x_c + r) and (pos_y < y_c): #  2°
             self.alpha1 = math.atan(m1) - math.pi
             self.alpha2 = math.atan(m2) - math.pi
        elif (x_c < pos_x < x_c + r) and (pos_y < y_c): #  2°
             self.alpha1 = math.atan(m1) - math.pi
             self.alpha2 = math.atan(m2)
        elif(pos_x < x_c - r) and (pos_y > y_c): # 3°
             self.alpha1 = math.atan(m1)
             self.alpha2 = math.atan(m2)
        elif (x_c -r < pos_x < x_c) and (pos_y > y_c):  # 3°
            self.alpha1 = math.atan(m1)
            self.alpha2 = math.atan(m2) + math.pi
        elif(pos_x > x_c + r) and (pos_y > y_c): # 4°
             self.alpha1 = math.atan(m1) + math.pi
             self.alpha2 = math.atan(m2) + math.pi
        elif (x_c < pos_x < x_c + r) and (pos_y > y_c):  # 4°
            self.alpha1 = math.atan(m1)
            self.alpha2 = math.atan(m2) + math.pi

        # in degrees
        alpha1 = self.alpha1 * 180 / math.pi
        alpha2 = self.alpha2 * 180 / math.pi

        if alpha1 < 0:
            alpha1 += 360
        if alpha2 < 0:
            alpha2 += 360

        # communication impact
        self.alpha_drone = math.atan2(pos_y - self.gs.y, pos_x - self.gs.x) * 180 / math.pi  # angolo tra drone e groundstation
        self.alpha_drone = self.alpha_drone + 180
        if (min(alpha1, alpha2) <= self.alpha_drone <= max(alpha1, alpha2)) and (self.distance_GS > distance_obstacle_GS):
            if type_object == 1:
                self.coeff = 0  # se coeff è uguale a 0 non c'è comunicazione
            elif type_object == 2:
                self.coeff = 0.5  # se coeff è uguale a 0.5 la comunicazione viene dimezzata
        else:
            self.coeff = 1

        #self.bitrate *= self.coeff
        return self.coeff
    def circle_color_fun(self):

        GREEN = (0, 255, 0, 200)
        ORANGE = (255, 128, 0, 200)
        RED = (255, 0, 0, 200)

        if self.bitrate == self.bitRate_max:
            self.circle_color = GREEN

        elif 0 < self.bitrate < self.bitRate_max:
                self.circle_color = ORANGE

        else:
                self.circle_color = RED

    def print_EndPoints(self, gs):
        i = 0
        print('Starting Position  x: %.2f, y: %.2f'%(gs.x, gs.y))
        for x, y in self.End_points:
            i +=1
            print('%d° End Point  x: %.2f, y: %.2f'%(i, x, y))
