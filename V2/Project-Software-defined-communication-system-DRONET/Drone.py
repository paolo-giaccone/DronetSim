import math
import random
import numpy as np
import queue

class Drone:
    def __init__(self, id, gs, T_lim, T_in, V_in, I_in, E, add_cons, Ej, mod_v_real, max_length_queue, N_missings):
        # waypoint coordinates
        self.x_new = 0
        self.y_new = 0
        # ground station
        self.gs = gs
        # UAV position: starting position same as the gs
        self.x = self.gs.x
        self.y = self.gs.y
        # number of iteration necessary to reach the waypoint
        self.tot_iterazioni = 0
        # UAV velocity
        self.mod_v_app = 13  # [m/s], constant velocity
        self.mod_v_real = mod_v_real # [m/s], resulting velocity
        # angle between the new direction and the horizontal
        self.teta = 0
        # remaining distance to reach the waypoint
        self.distance = 0
        # max available bitrate
        self.bitRate_max = 1e5 # bps
        # actual bitrate
        self.bitrate = self.bitRate_max
        # series of waypoints generated
        self.End_points = []
        # needed for ardupilot
        self.velocity = []
        # bitrate coefficient for attenuation
        self.coeff = 1
        # flag for the missing person
        self.found_missing_flag = np.zeros((N_missings, 1))
        # number of missing people found
        self.how_many_missing_are_found = np.zeros((N_missings, 1))

        ## UAV parameters
        self.T_lim = T_lim # [°C],limit temperature
        self.T_in = T_in  # [°C],initial temperature
        self.V_in = V_in  # [V], nominal voltage
        self.I_in = I_in  # [A], nominal current
        self.P = V_in * I_in # [W], power
        self.E = E # [Wh] initial energy
        self.Time_aut = self.P / self.E * 60  # fly time [min]
        self.add_cons = add_cons  # additional power consumption of the battery
        self.Ej = Ej  # initial battery energy in joule [J]
        self.Ej_check = Ej # it must be positive, otherwise the simulation ends

        self.id = id #drone ID
        # at Starting point there is no power consumption: we set them to 0
        self.act_cons = 0
        self.distance_GS = 0
        self.FLAG_PC = True # used as flag for available battery when changing between different temperature ranges (power consumption)

        # initial bitrate color circle
        GREEN = (0, 255, 0, 200)
        self.circle_color = GREEN

        # Available energy
        self.check_f = 0 # flag for Ej_check. When there is energy available it is set to 0

        # tangent angles
        self.alpha1 = 0
        self.alpha2 = 0
        self.alpha_drone = 0
        self.FLAG_Interrupt = True # the drone has battery level different from 0

######################################################################### DA VEDERE
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

    #########################################################################################

    def power_consumption(self, sample_T, T_amb):
        # Costant UAV speed. The power is invariant to the wind but change with temperature

        # initial values
        eta = 1  # coeff for power consumption
        alpha = 1  # coeff for available battery

        # Temperature range [20-40]°C
        if T_amb in range(self.T_lim, 2 * self.T_lim + 1):
            # best case for power consumption
            alpha = 1
            eta = 1

        # Temperature range [0-20]°C or > 40°C
        elif T_amb in range(0, self.T_lim) or T_amb > 2 * self.T_lim:

            if self.FLAG_PC:  # set available battery when changing the range for the first time. Then it is set to False (not updated)
                # battery efficiency decreases by increasing the difference between the ideal temperature and the T_amb
                alpha = 1 - 1 / 3 * (abs(self.T_lim - T_amb) / self.T_lim)
                self.FLAG_PC = False
            else:
                alpha = 1

            # if the temperature is under 20°C the power consumption is bigger
            eta = 1 + abs(self.T_lim - T_amb) * self.add_cons

        # Temperature range T < 0°C
        elif T_amb < 0:
            if self.FLAG_PC:  # set available battery when changing the range for the first time. Then it is set to False (not updated)
                # it is assumed that under 0°C the battery temperature remain constant
                alpha = 2 / 3
                self.FLAG_PC = False
            else:
                alpha = 1

            eta = 1 + abs(self.T_lim - T_amb) * self.add_cons

        # actual power consumption
        self.act_cons = eta * self.P * sample_T

        if not self.check_f:
            # updating of the battery energy every sample time
            self.Ej = alpha * self.Ej - self.act_cons
        else:
            # check if it is not negative
            self.Ej_check = alpha * self.Ej - self.act_cons


    def checkAvailabilityBattery(self, temperature, delta_T, Simulation):

        # percentage battery level
        battery_level = self.Ej * 100 / Simulation.Initial_Ej

        # worst case, battery decreases quicker if the temperature decreases (max possible decraese in temperature)
        deltaTemp_max = -1
        Temp_updated = temperature + deltaTemp_max

        # battery level below 20%
        if battery_level <= 20:
            self.check_f = 1
            self.power_consumption(delta_T, Temp_updated)
            battery_level_prov = self.Ej_check * 100 / Simulation.Initial_Ej
            if battery_level_prov < 0:
                # False to indicate loop should break
                self.FLAG_Interrupt = False
            else:
                # at the next Update UAV location event decrease the remaining battery level
                self.Ej_check = self.Ej
                self.check_f = 0
                self.FLAG_Interrupt = True


    def trajectory_UAV(self, x_shift, y_shift, n_cols, Waypoint, ARDUPILOT): # generation of next waypoint
        # standard settings: no Ardupilot
        if not ARDUPILOT:
            # set the specific subarea: division according to the number of UAV
            if self.id % n_cols == 0:
                i_x = n_cols # column
                i_y = self.id/n_cols # row

            elif self.id % n_cols != 0:
                i_x = self.id%n_cols # column
                i_y = np.ceil(self.id/n_cols) # row

            # relative position in the sub area: random choice
            self.x_new = random.uniform(0, 2*x_shift)
            self.y_new = random.uniform(0, 2*y_shift)

            # absolute position: considering the whole map
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

        # distance from the next waypoint
        delta_x_new = (self.x_new - self.x)
        delta_y_new = (self.y_new - self.y)
        self.distance = math.sqrt(delta_x_new ** 2 + delta_y_new ** 2)

        # angle between the new direction and the horizontal
        self.teta = math.atan2(delta_y_new, delta_x_new)

        # save all the waypoint generated for each UAV
        self.End_points.append((self.x_new, self.y_new))


    def cnt_iteration(self, time_slot):
        # distance from the next waypoint
        distance = math.sqrt((self.x_new - self.x) ** 2 + (self.y_new - self.y) ** 2)
        # time needed to reach the waypoint
        time_to_reach = distance / self.mod_v_real

        # compute the needed iteration to reach the waypoint
        if time_slot > 0:
            self.tot_iterazioni = np.round(time_to_reach / time_slot)


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

        # slope for linear decreasing region of Bitrate
        m = -self.bitRate_max / (2.5e3 - 2e3)

        # max bitrate region
        if self.distance_GS < 2e3:
            self.bitrate = self.bitRate_max

        # linear decreasing bitrate region
        elif 2e3 <= self.distance_GS < 2.5e3:
            self.bitrate = m * (self.distance_GS - 2e3) + self.bitRate_max

        # null bitrate region
        else:
            self.bitrate = 0

    def obstacle_fun(self, x_c, y_c, r, type_object, distance_obstacle_GS, scale_factor):
        # center and radius of the obstacle
        x_c *= scale_factor
        y_c *= scale_factor
        r *= scale_factor

        # UAV position
        pos_x = self.x*scale_factor
        pos_y = self.y*scale_factor

        # method used to find the tangent to the obstacle
        a = (x_c - pos_x) ** 2 - r ** 2
        b = 2 * (x_c * pos_y - pos_x * pos_y - x_c * y_c + pos_x * y_c)
        c = (y_c - pos_y) ** 2 - r ** 2

        Delta = b ** 2 - 4 * a * c
        # obstacle between the UAV and GS
        if Delta < 0:
            # mountain: on top of the mountain the communication is still available
            if type_object == 1:
                self.coeff = 1
            # cloud: it halves the bitrate
            elif type_object == 2:
                self.coeff = 0.5

            return self.coeff

        # "a" must be different from zero
        if a != 0:
            # tangent slopes
            m1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
            m2 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        elif a == 0:
            m1 = math.pi/2
            m2 = math.pi/2

        # checking the quadrants: the second conditions for each quadrant is related to the passage from one quadrant to another one
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

        # angles in degrees
        alpha1 = self.alpha1 * 180 / math.pi
        alpha2 = self.alpha2 * 180 / math.pi

        # angles in range [0-360]°
        if alpha1 < 0:
            alpha1 += 360
        if alpha2 < 0:
            alpha2 += 360

        # communication impact
        self.alpha_drone = math.atan2(pos_y - self.gs.y, pos_x - self.gs.x) * 180 / math.pi
        self.alpha_drone = self.alpha_drone + 180

        # if the obstacle is between the UAV and the GS
        if (min(alpha1, alpha2) <= self.alpha_drone <= max(alpha1, alpha2)) and (self.distance_GS > distance_obstacle_GS):
            # mountain obstacle
            if type_object == 1:
                # no communication available
                self.coeff = 0
            # cloud obstacle
            elif type_object == 2:
                # it halves the bitrate
                self.coeff = 0.5
        # no obstacles
        else:
            self.coeff = 1

        return self.coeff

    def circle_color_fun(self):
        # setting the colors for the circle on UAVs, representing the bitrate status
        GREEN = (0, 255, 0, 200)
        ORANGE = (255, 128, 0, 200)
        RED = (255, 0, 0, 200)

        # max bitrate: green
        if self.bitrate == self.bitRate_max:
            self.circle_color = GREEN

        # 0 < bitrate < max bitrate: orange
        elif 0 < self.bitrate < self.bitRate_max:
                self.circle_color = ORANGE

        # bitrate = 0: red
        else:
                self.circle_color = RED

    def print_EndPoints(self, gs):
        # to print all the waypoints
        i = 0
        print('Starting Position  x: %.2f, y: %.2f'%(gs.x, gs.y))
        for x, y in self.End_points:
            i +=1
            print('%d° End Point  x: %.2f, y: %.2f'%(i, x, y))
