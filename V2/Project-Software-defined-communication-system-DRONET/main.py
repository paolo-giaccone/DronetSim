### IMPORT OF USEFUL LIBRARIES ###

import math
import random
from queue import PriorityQueue
import matplotlib

import csv
import os.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygame
from scipy.stats import norm, t

### DEVELOPED CLASSES ###

from Drone import Drone
from relayUAV import Relay
from GroundStation import GroundStation
from Parameter_Initialization import Parameter_Initialization
from FES_management import FES_management
from Communication import Communication
from clouds import clouds
from DataAnalizer import data_analizer

##############################################################################

### PARAMETERS INITIALIZATION ###

## SIMULATION ##
TIME_SLOT = 2  # [s], time-step of the simulation
SCALE_FACTOR = 1.5  # mountain GS_distance 1600 m approx --> optimal value for scale_factor = 2
DELTA_t_ENV_CHANGE = 60 * 1  # [s], time for the environmental conditions updating

## DEFAULT PARAMETERS ##
T_AMB_PAR = 1  # [°C], initial environmental temperature
WIND_PAR = 10  # [m/s], initial wind velocity
GAMMA_PAR = math.pi  # initial wind angle

N_UAV_PAR = 10  # number of UAVs
N_clouds = 10  # number of clouds (obstacles)
N_missing = 5  # number of the missing persons that have to be found

## UAV PARAMETERS ##
Ej = 9.864e4 * 1.7  # [J], initial battery energy in joule
T_LIM = 20  # [°C], limit temperature for maximum battery efficiency
V_in = 53  # [V], nominal voltage
I_in = 5.9  # [A], nominal current
E = 274  # [Wh], initial energy in Watt per hour
MAX_MOD_WIND = 10  # [m/s], maximum value for the wind modulus
MAX_MOD_APPARENT_VELOCITY = 13  # [m/s], velocity of the drone, assumed constant
MIN_DISTANCE_WAYPOINTS = 100  # [m], minimum distance between the UAV and the next point to be reached
UAV_VISIBLE_RANGE = 100  # [m], maximum range of visibility of the missing person

## UAV COMMUNICATION PARAMETERS ##
MAX_LENGTH_QUEUE_UAV = 560  # maximum number of packets to full the queue
SIZE_PKT = 300 * 8  # [bit], packet size
SIZE_JSON = 160 * 8  # [bit], packet size for jason type
DELTA_t_MSG_TO_SENT = 4  # [s], every delta msg send a telemetry file
MAX_NUMB_OF_ATTEMPTIONS_TX_p0 = 3  # maximum number of retransmission attempts for low priority
MAX_NUMB_OF_ATTEMPTIONS_TX_p1 = 7  # maximum number of retransmission attempts for high priority

FLAG_double_channel = True  #choose if the channel between the UAV and the relay is the same of the one that tx toward the GS

## SIMULATION SETTINGS ##
SOUND = False  # sounds for the simulation
FLAG_debug = False  # debugging for the UAVs movement
DEFAULT_PARAMETERS = True  # default parameters
#FLAG_OS = 'Windows'  # needed for graph
FLAG_OS = 'MAC'
ARDUPILOT = False
FLAG_COMPUTE_THROUGHPUT = True

if FLAG_OS == 'MAC':
    matplotlib.use('Qt5Agg')  # importa il backend Qt5Agg


class Simulation():
    def __init__(self, seed):
        global TIME_SLOT
        global MAX_MOD_WIND
        global Ej
        global T_LIM
        global V_in
        global I_in
        global E
        global SCALE_FACTOR
        global N_missing
        global MIN_DISTANCE_WAYPOINTS
        global UAV_VISIBLE_RANGE
        global MAX_LENGTH_QUEUE_UAV
        global SIZE_PKT
        global SIZE_JSON
        global DELTA_t_ENV_CHANGE
        global DELTA_t_MSG_TO_SENT
        global DEFAULT_PARAMETERS
        global T_AMB_PAR
        global WIND_PAR
        global GAMMA_PAR
        global N_UAV_PAR
        global N_clouds
        global ARDUPILOT
        global FLAG_debug
        global FLAG_OS
        global FLAG_COMPUTE_THROUGHPUT
        global MAX_NUMB_OF_ATTEMPTIONS_TX_p0
        global MAX_NUMB_OF_ATTEMPTIONS_TX_p1
        global FLAG_double_channel

        ## Simulation Parameters Initialization
        # sample time for "Updating UAV position" event
        self.time_slot = TIME_SLOT
        self.Initial_Ej = Ej

        self.max_wind = MAX_MOD_WIND
        self.END_ARDUPILOT = True

        if DEFAULT_PARAMETERS:
            self.T_amb = T_AMB_PAR
            self.T_amb2 = T_AMB_PAR - 10

            self.wind = WIND_PAR
            self.wind2 = WIND_PAR

            self.gamma = GAMMA_PAR
            self.gamma2 = -GAMMA_PAR

            # Clouds
            self.N_clouds = N_clouds

            # Missing
            self.N_missing = N_missing

            # Ardupilot - Mission Planning
            self.ARDUPILOT = ARDUPILOT

            if self.ARDUPILOT:
                self.N_UAV = 1
            else:
                self.N_UAV = N_UAV_PAR

        else:
            Param_init = Parameter_Initialization(self.max_wind)

            # Initial temperature
            self.T_amb = Param_init.T_in1
            self.T_amb2 = Param_init.T_in2

            # Wind module
            self.wind = Param_init.wind1
            self.wind2 = Param_init.wind2

            # Wind Angle
            self.gamma = Param_init.gamma1
            self.gamma2 = Param_init.gamma2

            # Clouds
            self.N_clouds = Param_init.numb_clouds

            # Missing
            self.N_missing = Param_init.numb_missing

            # Ardupilot - Mission Planning
            self.ARDUPILOT = Param_init.ardupilot_flag

            # UAVs
            if self.ARDUPILOT:
                self.N_UAV = 1
            else:
                self.N_UAV = Param_init.numb_UAVs

            MAX_LENGTH_QUEUE_UAV = Param_init.Queue_Length
            MAX_NUMB_OF_ATTEMPTIONS_TX_p0 = Param_init.N_RetrAttemptLP
            MAX_NUMB_OF_ATTEMPTIONS_TX_p1 = Param_init.N_RetrAttemptHP

        # ARDUPILOT Planning
        if ARDUPILOT:
            self.Waypoints = pd.read_csv("./Ardupilot_Mission_Planning/Ardupilot Waypoints")
        else:
            self.Waypoints = None
        # graphs
        self.FLAG_graphs = True
        self.FLAG_debug = FLAG_debug

        # Ground Station
        self.GS_coord = [0, 0]
        self.gs = GroundStation(self.GS_coord[0], self.GS_coord[0], self.N_UAV)
        # FES
        self.FES = FES_management(SIZE_JSON, DELTA_t_MSG_TO_SENT, DELTA_t_ENV_CHANGE, N_UAV_PAR)
        # Data Analizer -> test&validation .csv
        self.data_analizer = data_analizer(self.FES, DELTA_t_MSG_TO_SENT)
        # Communication Class
        self.Communication = Communication(self.FES, self.gs, SIZE_JSON, SIZE_PKT, MAX_LENGTH_QUEUE_UAV, N_UAV_PAR,
                                           MAX_NUMB_OF_ATTEMPTIONS_TX_p0,
                                           MAX_NUMB_OF_ATTEMPTIONS_TX_p1, self.data_analizer, FLAG_double_channel)

        # UAVs
        self.UAVs = []
        self.UAV_Inizialization()
        self.delta_T = 0  # for power consumption
        self.numb_tot_bit_rx = 0
        self.numb_bit_rx_in_dt = 0
        self.numb_bit_generated_in_dt = 0
        self.numb_tot_bit_generated = 0
        self.time_channel_is_idle = 0
        self.time_channel_is_getting_busy = 0
        self.x_shift = 0
        self.y_shift = 0
        self.n_rows = 0
        self.n_cols = 0

        # missing
        self.missing_is_found = np.zeros((N_missing, N_UAV_PAR + 1))
        self.missing_person_found_flag = None

        # set the seed
        random.seed(seed)
        # simulation time
        self.sim_time = 0
        self.estimated_position = [-1, -1]

        # %% INITIALIZATION of the FES
        self.T_sample = 3  # 2 * self.time_slot  # [s] deve essere maggiore della granularity. Perchè?
        self.count_Sample_Time = 1
        self.FES.FES_Initialization(self.sim_time)
        self.tot_pkt_lost = 0
        self.pkt_lost_interval_time = 0
        # data pkt csv
        self.delta_time_for_throughput = 0

        # loop FLAG

        self.running = True

        # initialize the stats
        self.num_events = 0  # mi sa che non serve

        # Simulation Result DataFrame
        self.df = pd.DataFrame(
            columns=['Time_stamp [s]', 'id_drone', 'T_amb [°C]', 'T-right', 'T-left', 'wind speed [m/s]',
                     'wind angle[°]', 'position_x [m]',
                     'position_y [m]', 'UAV speed [m/s]', 'battery level [%]', 'actual consumption [Wh]',
                     'waypoint distance [m]', 'distance from GS [m]', 'bitrate [Mbps]', 'pkt lost tot',
                     'pkt lost missing', 'pkt lost iteration', 'pkt lost old'])

        # communication
        self.state_channel = 'idle'
        self.counter_iteration_per_each_UAV = np.zeros((self.N_UAV, 1))
        self.priority = 0
        self.type_of_file = None
        self.id_drone_send_file = -1
        self.time_past = 0
        self.pkts_UAV = np.zeros((2, self.N_UAV))
        self.latency_summation = 0
        self.n_pkt_received = 0
        self.n_tot_pkt_generated = 0
        self.n_pkt_generated_in_dt = 0

        self.clouds = []
        self.N_clouds = N_clouds

        # solo per 'stressare' il simulatore
        self.cnt_delta_msg = 1
        self.delta_msg_varying = DELTA_t_MSG_TO_SENT

        self.FLAG_exit_from_pygame = 0

    def UAV_Inizialization(self):
        add_cons = 0.02  # additional power consumption of the battery

        for i in np.arange(self.N_UAV):
            self.UAVs.append(Drone(i + 1, self.gs, T_LIM, self.T_amb, V_in, I_in, E, add_cons,
                                   Ej, MAX_MOD_APPARENT_VELOCITY, MAX_LENGTH_QUEUE_UAV, N_missing))

        # relay created
        self.relay = Relay(self.gs, T_LIM, self.T_amb, V_in, I_in, E, add_cons,
                           Ej, MAX_MOD_APPARENT_VELOCITY, MAX_LENGTH_QUEUE_UAV, SCALE_FACTOR, N_missing, N_UAV_PAR,
                           self.FES, DELTA_t_MSG_TO_SENT)

    def Start(self):

        # %% PyGame Model initialization
        pygame.init()

        # set screen dimension #
        info = pygame.display.Info()
        SCREEN_HEIGHT = info.current_h - 50
        self.SCREEN_WIDTH = info.current_w

        screen = pygame.display.set_mode((self.SCREEN_WIDTH, SCREEN_HEIGHT))

        # get a pygame clock object #
        clock = pygame.time.Clock()
        FPS = 60

        # load the images #
        background = pygame.image.load('background_1.jpg').convert()
        drone_image = pygame.image.load('drone2.png').convert_alpha()
        relay_image = pygame.image.load('relayUAV.png').convert_alpha()
        hotspot_img = pygame.image.load('hotspot.png').convert_alpha()
        GS_image = pygame.image.load('cr.jpg').convert()
        disperso_img = pygame.image.load('disperso.png').convert_alpha()
        wind_img = pygame.image.load('wind_image.png').convert_alpha()
        mountain_img = pygame.image.load('mountain.png').convert_alpha()
        mountain_img.set_alpha(200)
        cloud_img = pygame.image.load('cloud.png').convert_alpha()
        cloud_img.set_alpha(128)

        # Image Scaling #
        self.HEIGHT_controller = GS_image.get_height() - 52
        self.HEIGHT_game = SCREEN_HEIGHT - self.HEIGHT_controller
        background = pygame.transform.scale(background, (self.SCREEN_WIDTH, self.HEIGHT_game))

        # ArduPilot Waypoint control
        if ARDUPILOT:
            for i in range(self.Waypoints.shape[0]):
                x = self.Waypoints.iloc[i, 0]
                y = self.Waypoints.iloc[i, 1]

                if x > self.SCREEN_WIDTH:
                    self.Waypoints.iloc[i, 0] = self.SCREEN_WIDTH

                if y > self.HEIGHT_game:
                    self.Waypoints.iloc[i, 1] = self.HEIGHT_game
                    self.Waypoints = self.Waypoints.drop(self.Waypoints[self.Waypoints['y'] > self.HEIGHT_game].index)
                    break

        drone_size = 70
        relay_size = 100
        mountain_size = 400
        cloud_size = [300, 200]

        # clouds creation
        for i in range(self.N_clouds):
            cloud_pos_in = [random.randint(0, self.SCREEN_WIDTH), random.randint(0, self.HEIGHT_game)]
            self.clouds.append(
                clouds(cloud_pos_in[0], cloud_pos_in[1], self.SCREEN_WIDTH, self.HEIGHT_game))

        drone_image = pygame.transform.scale(drone_image, (drone_size, drone_size))
        relay_image = pygame.transform.scale(relay_image, (relay_size, relay_size))
        mountain_img = pygame.transform.scale(mountain_img, (mountain_size, mountain_size))
        cloud_img = pygame.transform.scale(cloud_img, (cloud_size[0], cloud_size[1]))

        # missing person #
        disperso_size = [100, 100]
        disperso_img = pygame.transform.scale(disperso_img, (disperso_size[0], disperso_size[1]))
        wind_img = pygame.transform.scale(wind_img, (0.7 * GS_image.get_width(), 0.7 * GS_image.get_height()))

        ## OBSTACLES

        # mountain
        Mountain_pos = [self.SCREEN_WIDTH / 2,
                        self.HEIGHT_game / 2 + self.HEIGHT_controller]  # uncomment in order to draw the circle on the mountain

        mountain_pos = (self.SCREEN_WIDTH / 2 - mountain_size / 2,
                        self.HEIGHT_game / 2 - mountain_size / 2 + self.HEIGHT_controller)  # position of the mountain
        self.Mountain_pos = (self.SCREEN_WIDTH / 2, self.HEIGHT_game / 2)
        self.mountain_radius = mountain_size / 2  # mountain radius
        self.mountain_type = 1

        # clouds parameters
        self.cloud_radius = (cloud_size[1] - 50) / 2
        self.cloud_type = 2

        h_d = disperso_img.get_height()
        w_d = disperso_img.get_width()

        # randomic coordinate for the missing
        self.coord_disperso = []
        for i in range(1, N_missing + 1):
            dist_coord = -1
            while (dist_coord <= self.mountain_radius + 200):
                if i%2 == 0:
                    x_disp = random.randint(20, self.SCREEN_WIDTH/2 - w_d*2)
                    y_disp = random.randint(10, self.HEIGHT_game - h_d*2)
                else:
                    x_disp = random.randint(self.SCREEN_WIDTH/2 + self.mountain_radius, self.SCREEN_WIDTH-w_d*2)
                    y_disp = random.randint(self.HEIGHT_game/2 + h_d*2, self.HEIGHT_game - h_d*2 )
                dist_coord = ((x_disp - self.Mountain_pos[0]) ** 2 + (y_disp - self.Mountain_pos[1]) ** 2) ** 0.5
            self.coord_disperso.append([x_disp + w_d / 2, y_disp + h_d / 2])
            print(self.coord_disperso)

        # Scaling factor h
        BLACK = (0, 0, 0)
        font = pygame.font.match_font('cour.ttf', bold=False, italic=False)
        font = pygame.font.SysFont(font, 30)
        text_surface_h = font.render('h: ' + str(self.HEIGHT_game * SCALE_FACTOR) + ' [m]', True, BLACK)

        SF_w = text_surface_h.get_width()
        SF_h = text_surface_h.get_height()
        SF_x_h = self.SCREEN_WIDTH - SF_w - 10
        SF_y_h = SCREEN_HEIGHT - SF_h - 10 - 2

        SF_display = pygame.Surface((SF_w + 10, 2 * SF_h + 10), pygame.SRCALPHA)  # per-pixel alpha
        SF_display.fill((80, 80, 80, 128))

        # Scaling factor w
        text_surface_w = font.render('w: ' + str(self.SCREEN_WIDTH * SCALE_FACTOR) + '[m]', True, BLACK)

        SF_x_w = self.SCREEN_WIDTH - SF_w - 10
        SF_y_w = SCREEN_HEIGHT - SF_h - 10 - text_surface_w.get_height() - 5

        SF_position = pygame.Vector2(SF_x_w - 5, SF_y_w - 5)

        # Wind Display #
        WP_w = wind_img.get_width()
        WP_h = wind_img.get_height()
        WP_x = self.SCREEN_WIDTH - WP_w - 10
        WP_y = self.HEIGHT_controller + 10

        WP_display = pygame.Surface((WP_w, WP_h), pygame.SRCALPHA)  # per-pixel alpha
        WP_display.fill((255, 255, 255, 128))
        WP_position = (WP_x, WP_y)
        WP_position_2 = (WP_x - self.SCREEN_WIDTH / 2, WP_y)

        # Arrow points for angle = 0
        points = [(WP_x + WP_w / 2, WP_y + WP_h / 2 - 5), (WP_x + WP_w - 15, WP_y + WP_h / 2 - 5),
                  (WP_x + WP_w - 15, WP_y + WP_h / 2 - 15),
                  (WP_x + WP_w, WP_y + WP_h / 2), (WP_x + WP_w - 15, WP_y + WP_h / 2 + 15),
                  (WP_x + WP_w - 15, WP_y + WP_h / 2 + 5), (WP_x + WP_w / 2, WP_y + WP_h / 2 + 5)]

        points_2 = [(WP_x - self.SCREEN_WIDTH / 2 + WP_w / 2, WP_y + WP_h / 2 - 5),
                    (WP_x - self.SCREEN_WIDTH / 2 + WP_w - 15, WP_y + WP_h / 2 - 5),
                    (WP_x - self.SCREEN_WIDTH / 2 + WP_w - 15, WP_y + WP_h / 2 - 15),
                    (WP_x - self.SCREEN_WIDTH / 2 + WP_w, WP_y + WP_h / 2),
                    (WP_x - self.SCREEN_WIDTH / 2 + WP_w - 15, WP_y + WP_h / 2 + 15),
                    (WP_x - self.SCREEN_WIDTH / 2 + WP_w - 15, WP_y + WP_h / 2 + 5),
                    (WP_x - self.SCREEN_WIDTH / 2 + WP_w / 2, WP_y + WP_h / 2 + 5)]

        points_speed = points
        points_speed_app = points

        # RIGHT - Environmental parameters
        BLACK = (0, 0, 0)
        font = pygame.font.match_font('Courier', bold=False, italic=False)
        font = pygame.font.SysFont(font, 30)

        text_surface_1 = font.render('Temperature left: %.1f°C' % (100), True, BLACK)
        text_surface_2 = font.render('Wind speed right: %.2f m/s, %.0f°' % (10, 180), True, BLACK)

        Text_width_r = max(text_surface_1.get_width() + 80, text_surface_2.get_width() + 80)
        Text_height_r = 2 * text_surface_2.get_height() + 9
        RP_x = self.SCREEN_WIDTH * 3 / 4 - Text_width_r / 2
        RP_y = 105 - 2

        Right_Position = pygame.Vector2(RP_x, RP_y)
        RP_display = pygame.Surface((Text_width_r + 10, Text_height_r + 10), pygame.SRCALPHA)  # per-pixel alpha
        RP_display.fill((80, 80, 80, 200))

        # LEFT - Environmental parameters
        BLACK = (0, 0, 0)
        font = pygame.font.match_font('Courier', bold=False, italic=False)
        font = pygame.font.SysFont(font, 30)

        text_surface_1 = font.render('Temperature left: %.1f°C' % (100), True, BLACK)
        text_surface_2 = font.render('Wind speed right: %.2f m/s, %.0f°' % (10, 180), True, BLACK)

        Text_width_l = max(text_surface_1.get_width() + 80, text_surface_2.get_width() + 80)
        Text_height_l = 2 * text_surface_2.get_height() + 9
        LP_x = self.SCREEN_WIDTH / 4 - Text_width_l / 2 + 20
        LP_y = 105 - 2

        Left_Position = pygame.Vector2(LP_x, LP_y)
        LP_display = pygame.Surface((Text_width_l + 10, Text_height_l + 10), pygame.SRCALPHA)  # per-pixel alpha
        LP_display.fill((80, 80, 80, 200))

        # Starting Position of the Drone #
        # update position of GS (now we know the size of the screen)

        Start_position = pygame.Vector2(self.GS_coord[0], self.GS_coord[1] + self.HEIGHT_controller)

        # Set the size of the circle
        circle_radius = drone_size * 15 / 100  # 10:100 = x: drone_size
        circle_radius1 = relay_size * 15 / 100  # 10:100 = x: drone_size
        # Create a surface for the circle
        circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
        circle_surface1 = pygame.Surface((circle_radius1 * 2, circle_radius1 * 2), pygame.SRCALPHA)

        # UAV image
        self.h_drone = drone_size
        self.w_drone = drone_size

        # distance between mountain and ground station
        self.distance_M_GS = math.sqrt((self.Mountain_pos[0] - self.gs.x) ** 2 +
                                       (self.Mountain_pos[1] - self.gs.y) ** 2) * SCALE_FACTOR

        if SOUND:
            # loading sound #
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
            self.communication_sound = pygame.mixer.Sound("beep-08b.mp3")
            self.find_sound = pygame.mixer.Sound("beep-21.mp3")
            self.destination_reached_sound = pygame.mixer.Sound("destination reached.mp3")

        # first tangent evaluation
        for drone in self.UAVs:
            for cloud_each in self.clouds:
                coef_obstacl = drone.obstacle_fun(cloud_each.cloud_x, cloud_each.cloud_y, self.cloud_radius, self.cloud_type,
                                   cloud_each.distance_C_GS, SCALE_FACTOR)
                drone.bitrate *= coef_obstacl
            # for the mountain
            coef_obstacl = drone.obstacle_fun(self.Mountain_pos[0], self.Mountain_pos[1], self.mountain_radius, self.mountain_type,
                               self.distance_M_GS, SCALE_FACTOR)
            drone.bitrate *= coef_obstacl

        self.AreaDivision()

        # pygame window start
        while self.running:

            # pygame.QUIT event means the user clicked X to close your window #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # FES Event Loop
            while (not self.FES.FES.empty()) and len(self.UAVs) > 0 and self.FLAG_exit_from_pygame == 0:
                self.EventLoop()
                # Update Frame
                screen.blit(background, [0, self.HEIGHT_controller])
                screen.blit(GS_image, Start_position)
                cnt = 0
                font1 = pygame.font.match_font('Courier', bold=False, italic=False)
                font1 = pygame.font.SysFont(font1, 30)
                for coord_missing in self.coord_disperso:
                    screen.blit(disperso_img, [coord_missing[0], self.HEIGHT_controller + coord_missing[1]])
                    ID = font1.render(str(cnt), True, [128, 0, 0])
                    screen.blit(ID, (int(coord_missing[0] + disperso_size[0] / 2 - 30),
                                     int(self.HEIGHT_controller + coord_missing[1] + disperso_size[1] / 2 - 41)))
                    cnt += 1
                screen.blit(mountain_img, mountain_pos)
                for cloud_cl in self.clouds:
                    cloud_pos = [int(cloud_cl.cloud_x - cloud_size[0] / 2),
                                 int(self.HEIGHT_controller + cloud_cl.cloud_y - cloud_size[1] / 2)]
                    screen.blit(cloud_img, (cloud_pos[0], cloud_pos[1]))
                    if self.FLAG_debug:
                        pygame.draw.circle(screen, (0, 0, 0),
                                           (cloud_pos[0] + cloud_size[0] / 2, cloud_pos[1] + cloud_size[1] / 2),
                                           self.cloud_radius, 2)  # for the tangents
                # separation line
                pygame.draw.line(screen, (0, 0, 0, 200), (self.Mountain_pos[0], self.HEIGHT_controller),
                                 (self.Mountain_pos[0], SCREEN_HEIGHT), 2)

                # circle for debugging
                if self.FLAG_debug:
                    pygame.draw.circle(screen, (0, 0, 155), (Mountain_pos[0], Mountain_pos[1]), self.mountain_radius,
                                       5)  # for the tangents

                for drone in self.UAVs:
                    screen.blit(drone_image,
                                (int(drone.x - drone_size / 2), int(self.HEIGHT_controller + drone.y - drone_size / 2)))

                    # Position_Hotspot = [drone.x_new - hotspot_img.get_width() / 2,
                    #                   self.HEIGHT_controller + drone.y_new - hotspot_img.get_height() / 2]

                    # screen.blit(hotspot_img, Position_Hotspot)

                    # Draw the circle on the circle surface
                    pygame.draw.circle(circle_surface, drone.circle_color, (circle_radius, circle_radius),
                                       circle_radius)

                    # Flash the circle if the current time is within the flash interval
                    screen.blit(circle_surface,
                                (int(drone.x - circle_radius),
                                 int(self.HEIGHT_controller + drone.y - circle_radius)))

                    # id drone
                    ID = font1.render(str(drone.id), True, BLACK)
                    screen.blit(ID, (int(drone.x - circle_radius + 5),
                                     int(self.HEIGHT_controller + drone.y - circle_radius)))

                    # rette tangenti
                    if self.FLAG_debug:
                        r = self.SCREEN_WIDTH / 2
                        Start_position_ = [drone.x, self.HEIGHT_controller + drone.y]

                        End_Position_m1 = [r * math.cos(drone.alpha1) + Start_position_[0],
                                           r * math.sin(drone.alpha1) + Start_position_[1]]
                        End_Position_m2 = [r * math.cos(drone.alpha2) + Start_position_[0],
                                           r * math.sin(drone.alpha2) + Start_position_[1]]
                        End_Position_gs = [
                            r * math.cos(drone.alpha_drone / 180 * math.pi) + Start_position_[0],
                            r * math.sin(drone.alpha_drone / 180 * math.pi) + Start_position_[1]]

                        pygame.draw.line(screen, (255, 0, 0), Start_position_, End_Position_m1, 4)
                        pygame.draw.line(screen, (255, 0, 0), Start_position_, End_Position_m2, 4)
                        pygame.draw.line(screen, (255, 255, 0), Start_position_, End_Position_gs, 4)

                # relay UAV display
                screen.blit(relay_image, (int(self.relay.drone.x - relay_size / 2),
                                          int(self.HEIGHT_controller + self.relay.drone.y - relay_size / 2)))
                pygame.draw.circle(circle_surface1, self.relay.drone.circle_color, (circle_radius1, circle_radius1),
                                   circle_radius1)
                screen.blit(circle_surface1, (int(self.relay.drone.x - circle_radius1),
                                              int(self.HEIGHT_controller + self.relay.drone.y - circle_radius1)))

                if self.FLAG_debug:
                    r = self.SCREEN_WIDTH / 2

                    Start_position_ = [self.relay.drone.x, self.HEIGHT_controller + self.relay.drone.y]

                    End_Position_gs = [
                        r * math.cos(self.relay.drone.alpha_drone / 180 * math.pi) + Start_position_[0],
                        r * math.sin(self.relay.drone.alpha_drone / 180 * math.pi) + Start_position_[1]]

                    pygame.draw.line(screen, (255, 255, 0), Start_position_, End_Position_gs, 4)

                # screen scale factor display
                screen.blit(SF_display, SF_position)
                screen.blit(text_surface_h, (SF_x_h, SF_y_h))
                screen.blit(text_surface_w, (SF_x_w, SF_y_w))

                # wind display right
                screen.blit(WP_display, WP_position)
                screen.blit(wind_img, WP_position)
                screen.blit(RP_display, Right_Position)

                # wind display left
                screen.blit(WP_display, WP_position_2)
                screen.blit(wind_img, WP_position_2)
                screen.blit(LP_display, Left_Position)

                wind_color = round(255 - 255 * self.wind / self.max_wind)
                pygame.draw.polygon(screen, [255, wind_color, 255],
                                    self.rotatePolygon(points, self.gamma, WP_x, WP_w, WP_y, WP_h))

                wind_color2 = round(255 - 255 * self.wind2 / self.max_wind)
                pygame.draw.polygon(screen, [255, wind_color2, 0],
                                    self.rotatePolygon(points_2, self.gamma2, WP_x - self.SCREEN_WIDTH / 2, WP_w, WP_y,
                                                       WP_h))

                if FLAG_debug:
                    for drone in self.UAVs:
                        # effective direction
                        pygame.draw.polygon(screen, [255, 205, 42],
                                            self.rotatePolygon(points_speed, drone.teta, WP_x, WP_w, WP_y, WP_h))
                        # apperent direction
                        pygame.draw.polygon(screen, [0, 0, 255],
                                            self.rotatePolygon(points_speed_app, drone.ang_v_app, WP_x, WP_w, WP_y,
                                                               WP_h))

                # Update the "pc screen" #
                self.gs.pc_controller(screen, self.estimated_position, self.SCREEN_WIDTH)

                # Update the simulation information #
                self.text_controller(screen)

                # flip the display to put your work on screen #
              #  pygame.display.flip()

                # updating image rate #
                clock.tick(FPS)

            # graphs

            self.running = False
            self.graphs()
            print('\nThroughput tot: ', self.data_analizer.THROUGHPUT_tot,
                  '\t Throughput relay: ', self.data_analizer.THROUGHPUT_relay,
                  '\t Throughput UAV: ',self.data_analizer.THROUGHPUT_UAVs)

            print('\nLatency relay: ', self.data_analizer.latency_relay,
                  '\t Latency UAVs: ', self.data_analizer.latency_UAVs)

            print('\nPktlost tot: ', self.data_analizer.lost_pkt_tot_bps,
                  '\t Throughput relay: ', self.data_analizer.lost_pkt_relay,
                  '\t Throughput UAV: ', self.data_analizer.lost_pkt_UAVs, '\n')

        # for debug #
        # print("\n\nTotal number of events: ", num_events)
        # print("Current Energy: ", drone.Ej/3600, "[Wh]")
        # print("Current Simulation Time: %.2f [s]"%sim_time)
        # drone.print_EndPoints(gs)

        # end
        pygame.quit()

    def search_UAVs_index(self, identification):
        index = 0
        for h in range(0, len(self.UAVs)):
            if self.UAVs[h].id == identification:
                index = h
        #        print('\nMATCH identification %d and ID %d\n'%(identification, self.UAVs[h].id))
        return index

    def during_communication_update_position(self):
        # update the position (in this way we know the current bitrate)
        time_interval = self.sim_time - self.time_past
        if time_interval > 0:
            self.update_UAV_location(time_interval)
        self.time_past = self.sim_time

    def search_the_UAV_transmitter(self, identification):
        (gen_time, state, queue_owner, pkt_owner, type_pkt, size_pkt, priority_of_pkt, cnt_packet_sent,
         total_pkt, pkt_id) = identification
        if queue_owner == 'relay':
            UAV = self.relay
        else:
            index = self.search_UAVs_index(type_pkt)
            UAV = self.UAVs[index]
        return UAV

    def EventLoop(self):
        # FES event loop #
        # get the event
        tuple_FES = self.FES.read_event()
        (time, self.event_type, identification) = tuple_FES

        # update the stats
        self.num_events += 1
       # self.delta_T = self.time_slot
        self.delta_T = time - self.sim_time
        # update the current time
        self.sim_time = time

        match self.event_type:
            # Choose the next destination point
            case "Choice of the trajectory":
                self.Choice_of_the_trajectory(identification)

            # move towards the evaluated destination point -- one event for all UAVs
            case 'update UAV location':
                self.update_UAV_location(self.delta_T)

            # Change Wind and Temperature simulation periodically
            case 'Change environmental effects':
                self.Change_environmental_effects()

            case 'Sampling':
                self.Sampling()

            # coordination or image send to the Ground Station
            case 'Send Rescues Datas':
                id_dr, ID_missing = identification
                self.during_communication_update_position()
                index = self.search_UAVs_index(id_dr)
                if index < len(self.UAVs):
                    print('\n SimTime: ', self.sim_time, '\n Event: ', self.event_type, '\n Drone: ',
                          self.UAVs[index].id,
                          '\n Size Queue: ', self.UAVs[index].queue.qsize(), '\n Bitrate: ', self.UAVs[index].bitrate,
                          '\n')

                    self.Communication.sending_data_of_missings(self.UAVs[index], self.relay, self.sim_time,
                                                                self.delta_msg_varying)
                self.estimated_position = [self.UAVs[index].x, self.UAVs[index].y]

            case 'Send Telemetry Data':
                self.during_communication_update_position()
                index = self.search_UAVs_index(identification)
                if index < len(self.UAVs):
                    if self.relay.FLAG_ARRIVED:
                        print('\n SimTime: ', self.sim_time, '\n Event: ', self.event_type, '\n Drone: ',
                              self.UAVs[index].id,
                              '\n Size Queue: ', self.UAVs[index].queue.qsize(), '\n Bitrate: ', self.UAVs[index].bitrate,
                              '\n')

                        self.Communication.sending_telemetry_data(self.UAVs[index], self.relay, self.sim_time,
                                                                  self.delta_msg_varying)
                        # schedule the new tx event
                        self.FES.add_events(self.sim_time + DELTA_t_MSG_TO_SENT, "Send Telemetry Data", self.UAVs[index].id)
                        # if self.sim_time > self.cnt_delta_msg * 60 and self.sim_time > 150:
                        #   self.cnt_delta_msg += 1
                        #  self.delta_msg_varying = self.delta_msg_varying / 2
                    # self.FES.add_events(self.sim_time + self.delta_msg_varying, "Send Telemetry Data",
                    #                    self.UAVs[index].id)

            case 'Transmission attempt':
                self.during_communication_update_position()
                (UAV_sender_id, type_pkt, size_pkt, priority_of_pkt) = identification
                index = self.search_UAVs_index(UAV_sender_id)
                if UAV_sender_id == 0:
                    print('\n SimTime: ', self.sim_time, '\n Event: ', self.event_type, '\n Drone: ', UAV_sender_id,
                          '\n Size Queue: ', self.relay.queue.qsize(), '\n Bitrate: ', self.UAVs[index].bitrate, '\n')

                    self.Communication.channel_communication(self.relay, None, self.sim_time, self.delta_msg_varying)
                else:
                    if index < len(self.UAVs):
                        if self.UAVs[index].bitrate == 0:
                            print('\n 1SimTime: ', self.sim_time, '\n Event: ', self.event_type, '\n Drone: ',
                                  self.UAVs[index].id,'the bit rate is: ', self.UAVs[index].bitrate, 'the queue size is: ',
                                  self.UAVs[index].queue.qsize(),' check bit rate has to be called')
                            self.Communication.bitrate_null_send_to_relay(self.UAVs[index], self.relay, self.sim_time,
                                                                self.delta_msg_varying, type_pkt, size_pkt, priority_of_pkt)
                        else:
                            print('\n 2SimTime: ', self.sim_time, '\n Event: ', self.event_type, '\n Drone: ',
                                  self.UAVs[index].id,
                                  '\n Size Queue: ', self.UAVs[index].queue.qsize(), '\n Bitrate: ',
                                  self.UAVs[index].bitrate, '\n')
                            self.Communication.channel_communication(self.UAVs[index], self.relay, self.sim_time,
                                                                     self.delta_msg_varying)

            case 'Transmission attempt toward relay':
                self.during_communication_update_position()
                (UAV_sender_id, type_pkt, size_pkt, priority_of_pkt) = identification
                index = self.search_UAVs_index(UAV_sender_id)
                print('\n SimTime: ', self.sim_time, '\n Event: ', self.event_type, '\n Drone: ',
                      self.UAVs[index].id,
                      '\n Size Queue: ', self.UAVs[index].queue.qsize(), '\n Bitrate: ', self.UAVs[index].bitrate,
                      '\n')
                self.Communication.tx_from_UAV_toward_RELAY(self.UAVs[index], self.relay, self.sim_time,
                                                            self.delta_msg_varying, type_pkt, size_pkt, priority_of_pkt)

            case 'Relay: Received pkt from UAV':
                self.during_communication_update_position()
                index = self.search_UAVs_index(identification)
                print('\n SimTime: ', self.sim_time, '\n Event: ', self.event_type, '\n Drone: ',
                      self.UAVs[index].id,
                      '\n Size Queue: ', self.UAVs[index].queue.qsize(), '\n Bitrate: ', self.UAVs[index].bitrate,
                      '\n')
                self.Communication.Relay_rx_pkt_from_UAV(self.UAVs[index], self.relay, self.sim_time, self.delta_msg_varying)

            case 'Received Data':
                #print('\n SimTime: ', self.sim_time, '\n Event: ', self.event_type, '\n Drone: ', identification, '\n')
                UAV_tx = self.search_the_UAV_transmitter(identification)
                if UAV_tx.id == 0 and not self.relay.flag_start_TX:
                    self.relay.flag_start_TX = True
                self.Communication.received_data(identification, UAV_tx, self.sim_time, self.delta_msg_varying)
                #print('RECEIVED DATA MAIN: sim time: ', self.sim_time)

    def Choice_of_the_trajectory(self, id_drone):

        i_x = 1  # subarea column
        i_y = 1  # subarea row

        for drone in self.UAVs:
            # for all UAVs
            if id_drone == -1 and not ARDUPILOT:  # only at the first time, move the UAVs to the center of the respective subarea
                # set the end point at the center of the respective subarea
                drone.first_position(self.x_shift, self.y_shift, i_x, i_y)

                # change the specific subarea for each UAV
                if i_x == self.n_cols:
                    i_x = 1
                    i_y += 1
                else:
                    i_x += 1

                # compute the needed iterations to reach the generated waypoint
                drone.cnt_iteration(self.time_slot)

                # update the effective velocity of the drone
                (T, w, wind_angle, flag_pos) = self.check_position(drone.x)
                drone.velocity_real(w, wind_angle)

                if drone.id == 1:
                    drone.velocity.append(drone.mod_v_real)


            # for a specific UAV
            elif drone.id == id_drone:
                if not ARDUPILOT:
                    pos = None
                elif self.Waypoints.shape[0] != 0:
                    pos = self.Waypoints.iloc[0].to_numpy()
                    pos = pos[1:]

                    self.Waypoints = self.Waypoints.drop(self.Waypoints.index[0])
                    self.Waypoints.reset_index(drop=True, inplace=True)
                elif self.END_ARDUPILOT:
                    pos = [0, 0]
                    self.END_ARDUPILOT = False
                else:
                    drone.FLAG_Interrupt = False
                    pos = [0, 0]
                drone.trajectory_UAV(self.x_shift, self.y_shift, self.n_rows, self.n_cols, pos, ARDUPILOT)

                # compute the needed iterations to reach the generated waypoint
                drone.cnt_iteration(self.time_slot)

                # update the effective velocity of the drone
                (T, w, wind_angle, flag_pos) = self.check_position(drone.x)
                drone.velocity_real(w, wind_angle)

                if drone.id == 1:
                    drone.velocity.append(drone.mod_v_real)

        # schedule a new event # - the same for all UAVs
        if id_drone == -1:
            self.FES.add_events(self.sim_time + self.time_slot, 'update UAV location', -1)

    def AreaDivision(self):
        N = self.N_UAV  # without the UAV relay
        Width = self.SCREEN_WIDTH
        Height = self.HEIGHT_game

        max_div_1 = math.sqrt(N)
        # first number
        max_ = 1
        for i in range(1, int(np.floor(max_div_1) + 1)):
            if N % i == 0 and max_ < i:
                max_ = i
        # second number
        mult = N / max_

        # col = max number, row = min number
        self.n_rows = min(mult, max_)
        self.n_cols = max(mult, max_)

        # shift to the center of the subareas
        self.x_shift = (Width / self.n_cols) / 2
        self.y_shift = (Height / self.n_rows) / 2

    def update_UAV_location(self, time_interval):

   #     print('\nTIME INTERVAL: ', time_interval)

        # relay movement
        if not self.relay.FLAG_ARRIVED:
            (T, w, wind_angle, flag_pos) = self.check_position(self.relay.drone.x)
            self.relay.veloc_real(w, wind_angle, self.Mountain_pos[0], self.Mountain_pos[1])
            self.relay.reach_top_mountain(time_interval)

        # move each cloud
        for cloud_each in self.clouds:
            (T, w, wind_angle, flag_pos) = self.check_position(cloud_each.cloud_x)
            cloud_each.cloud_motion(time_interval, self.GS_coord[0], self.GS_coord[1], SCALE_FACTOR, w, wind_angle)
        # evaluate the current Bit_Rate in function of the distance #
        self.relay.drone.bitrate_fun(SCALE_FACTOR)
        # obstacles effect on the bit rate #
        for cloud_each in self.clouds:
            coef_obstacl = self.relay.drone.obstacle_fun(cloud_each.cloud_x, cloud_each.cloud_y, self.cloud_radius, self.cloud_type,
                                          cloud_each.distance_C_GS, SCALE_FACTOR)
            self.relay.drone.bitrate *= coef_obstacl
        # relay bitrate color
        self.relay.drone.circle_color_fun()

        # loop for each UAV
        for drone in self.UAVs:
            # In which side with respect the mountain the UAV is
            (T, w, wind_angle, flag_pos) = self.check_position(drone.x)

            # destination not reached
            if drone.tot_iterazioni > 0:
                # print('\nID: ', drone.id, ' DELTA Time: ', time_interval, '\n\n')

                # move the drone #
                drone.move(time_interval)

                # compute the needed iterations to reach the generated waypoint
                if time_interval > 0:
                    drone.cnt_iteration(time_interval)

                # Bit Rate #
                # evaluate the current Bit_Rate in function of the distance
                drone.bitrate_fun(SCALE_FACTOR)
                # account the obstacle for the bit-rate. Each obstacle counts.
                # clouds
                for cloud_each in self.clouds:
                    coef_obstacl = drone.obstacle_fun(cloud_each.cloud_x, cloud_each.cloud_y, self.cloud_radius, self.cloud_type,
                                       cloud_each.distance_C_GS, SCALE_FACTOR)
                    # update bitrate for the 2nd channel (relay-UAV)
                    self.bitrate_null_Relay_UAV(drone, self.Mountain_pos, cloud_each.cloud_x, cloud_each.cloud_y)
                    drone.bitrate *= coef_obstacl
                # mountain
                coef_obstacl = drone.obstacle_fun(self.Mountain_pos[0], self.Mountain_pos[1], self.mountain_radius,
                                   self.mountain_type, self.distance_M_GS, SCALE_FACTOR)
                drone.bitrate *= coef_obstacl
                # update the bit rate state in the map
                drone.circle_color_fun()



                # find missing person #
                drone_center = (drone.x + self.w_drone / 2, drone.y + self.h_drone / 2)

                cnt = 0
                for coord_missing in self.coord_disperso:
                    distance = math.sqrt((drone_center[0] - coord_missing[0]) ** 2 +
                                         (drone_center[1] - coord_missing[1]) ** 2)

                    # the missing person and the UAV are in range of visibility

                    if distance <= UAV_VISIBLE_RANGE and self.relay.FLAG_ARRIVED and \
                            cnt != self.missing_person_found_flag and self.relay.flag_start_TX:
                        if drone.found_missing_flag[cnt] == 0:
                           # print('coord disperso: ( %d, %d ), coord UAV: ( %d, %d ), distance: %.2f and drone ID: %d\n' % (
                          #      coord_missing[0], coord_missing[1], drone.x, drone.y, distance, drone.id))
                         #   print('DRONE_ID: %d the missing %d is under my field of view\n' % (drone.id, cnt))
                            self.FES.add_events(self.sim_time, 'Send Rescues Datas', (drone.id, cnt))
                            drone.found_missing_flag[cnt] = 1
                            drone.how_many_missing_are_found[cnt] = 1
                            self.missing_is_found[cnt][drone.id] = 1
                            self.missing_person_found_flag = cnt
                          #  print('\nDRONE: ', drone.id,
                          #        ' Send Rescues Datas event is inserted in the FES and the distance is : ',
                           #       distance, 'and simtime: ', self.sim_time, 'and the ID of person is: ', cnt, '\n')
                    else:
                        drone.found_missing_flag[cnt] = 0
                    cnt += 1

                # update the number of iteration #
                drone.tot_iterazioni -= 1


            # destination reached #
            else:
                if SOUND:
                    self.destination_reached_sound.play()
                # schedule a new event #
                self.FES.add_events(self.sim_time, 'Choice of the trajectory', drone.id)
                # print("\nID: ", drone.id, "NUMERO Iterazioni: ", drone.tot_iterazioni, '\n')

            # True if the remaining battery level is not negative
            drone.checkAvailabilityBattery(T, self.time_slot, self)
            # update the remaining power #
            drone.power_consumption(time_interval, self.check_position(drone.x)[0])

            # print('ciao 3', drone.Ej, drone.Ej_check, drone.id, drone.FLAG_Interrupt, drone.tot_iterazioni)
            if not drone.FLAG_Interrupt:
                if drone.id > 0:
                    print("Goodbye drone ID: ", drone.id, )
                    print('\nThroughput tot: ', self.data_analizer.THROUGHPUT_tot,
                          '\t Throughput relay: ', self.data_analizer.THROUGHPUT_relay,
                          '\t Throughput UAV: ', self.data_analizer.THROUGHPUT_UAVs)

                    print('\nLatency relay: ', self.data_analizer.latency_relay,
                          '\t Latency UAVs: ', self.data_analizer.latency_UAVs)

                    print('\nPktlost tot: ', self.data_analizer.lost_pkt_tot_bps,
                          '\t Throughput relay: ', self.data_analizer.lost_pkt_relay,
                          '\t Throughput UAV: ', self.data_analizer.lost_pkt_UAVs, '\n')
                    if len(self.UAVs) == 1:
                        self.Ej_UAV = drone.Ej

                    # to ArduPilot
                    if drone.id == 1:
                        Waypoints = pd.DataFrame(drone.End_points, columns=['x', 'y'])
                        Waypoints['abs velocity'] = drone.velocity
                        Waypoints.to_csv('Waypoints_first_UAV')

                    self.UAVs = list(filter(lambda x: x.id != drone.id, self.UAVs))
                    self.FES.remove_events(drone.id, 'all')
                    self.FLAG_exit_from_pygame = 1
                else:
                    print("Invalid drone ID: ", drone.id)

        # needed for communication
        if self.event_type == 'update UAV location':
            # schedule new event
            self.FES.add_events(self.sim_time + self.time_slot, 'update UAV location', -1)
            self.time_past = self.sim_time

    def Change_environmental_effects(self):
        # change Temperature
        self.T_amb = self.T_amb + random.randint(-10, 10) / 10  # [K]
        # change wind
        self.gamma = random.uniform(-math.pi, math.pi)  # [rad]
        self.wind = random.uniform(0, 10)  # [m/s]

        self.T_amb2 = self.T_amb2 + random.randint(-10, 10) / 10  # [K]
        # change wind
        self.gamma2 = random.uniform(-math.pi, math.pi)  # [rad]
        self.wind2 = random.uniform(0, 10)  # [m/s]

        # battery level updating
        for drone in self.UAVs:
            self.check_environmental_eff_worst_case(drone)
        self.check_environmental_eff_worst_case(self.relay.drone)

        # update the  effective velocity of each UAV
        for drone in self.UAVs:
            (T, w, wind_angle, flag_pos) = self.check_position(drone.x)
            drone.velocity_real(w, wind_angle)

        # update the  effective velocity of the UAV realy
        (T, w, wind_angle, flag_pos) = self.check_position(self.relay.drone.x)
        self.relay.veloc_real(w, wind_angle, self.Mountain_pos[0], self.Mountain_pos[1])

        # add or remove clouds randomly
        # 0-> remove, 1-> add
        add_or_rem = random.randint(0, 2)
      #  print('add_or_remove: ', add_or_rem)

        if add_or_rem == 1:  # add n clouds
            # random numb of clouds to add or remove
            n_to_add_or_remove = random.randint(0, 2)  # len(self.clouds) + 4)
     #       print('n_to_add_or_remove: ', n_to_add_or_remove)
            for _ in range(n_to_add_or_remove):
                cloud_pos_in = [random.randint(0, self.SCREEN_WIDTH), random.randint(0, self.HEIGHT_game)]
                new_cloud = clouds(cloud_pos_in[0], cloud_pos_in[1], self.SCREEN_WIDTH,
                                   self.HEIGHT_game)  # Crea una nuova istanza di Nuvola
                self.clouds.append(new_cloud)  # Aggiungi la nuova nuvola alla lista
      #      print('clouds added, length list: ', len(self.clouds))
        elif add_or_rem == 0:  # remove n
            # random numb of clouds to add or remove
            n_to_add_or_remove = random.randint(0, 2)  # len(self.clouds))
       #     print('n_to_add_or_remove: ', n_to_add_or_remove)
       #     print('n_to_add_or_remove: ', n_to_add_or_remove)
            # remove some clouds
            for _ in range(n_to_add_or_remove):
                if len(self.clouds) > 0:
                    cloud_to_be_removed = random.choice(self.clouds)  # choose a randomic cloud from the list
                    self.clouds.remove(cloud_to_be_removed)  # remove
        #    print('clouds removed, length list: ', len(self.clouds))

    def bitrate_null_Relay_UAV(self, drone, Mountain_pos, cloud_x, cloud_y):
        self.relay.bitrate_relay_UAV(drone.x, drone.y, Mountain_pos)
        drone.bitrate_Relay_UAV = self.relay.bitrate_UAV_rel
        for cloud_each in self.clouds:
            # distance between mountain and cloud
            distance_C_relay = math.sqrt((cloud_x - Mountain_pos[0]) ** 2 + (cloud_y - Mountain_pos[1]) ** 2) * SCALE_FACTOR

            coef_obstacl = self.relay.drone.obstacle_fun(cloud_each.cloud_x, cloud_each.cloud_y, self.cloud_radius,
                                              self.cloud_type,
                                              distance_C_relay, SCALE_FACTOR)

            drone.bitrate_Relay_UAV *= coef_obstacl

    def check_environmental_eff_worst_case(self, drone):
        # control in which part of the screen the UAV is
        (T, w, wind_angle, flag_pos) = self.check_position(drone.x)

        # update the power consumption before changing the environmental effect
        drone.checkAvailabilityBattery(T, self.time_slot, self)
        drone.power_consumption(self.delta_T, self.check_position(drone.x)[0])

        if not drone.FLAG_Interrupt:
            if drone.id > 0:
                print("Goodbye drone ID: ", drone.id, )
                print('\nThroughput tot: ', self.data_analizer.THROUGHPUT_tot,
                      '\t Throughput relay: ', self.data_analizer.THROUGHPUT_relay,
                      '\t Throughput UAV: ', self.data_analizer.THROUGHPUT_UAVs)

                print('\nLatency relay: ', self.data_analizer.latency_relay,
                      '\t Latency UAVs: ', self.data_analizer.latency_UAVs)

                print('\nPktlost tot: ', self.data_analizer.lost_pkt_tot_bps,
                      '\t Throughput relay: ', self.data_analizer.lost_pkt_relay,
                      '\t Throughput UAV: ', self.data_analizer.lost_pkt_UAVs, '\n')
                if len(self.UAVs) == 1:
                    self.Ej_UAV = drone.Ej
                self.UAVs = list(filter(lambda x: x.id != drone.id, self.UAVs))
                self.FES.remove_events(self.FES, 'all')
                self.FLAG_exit_from_pygame = 1
            else:
                print("Invalid drone ID: ", drone.id)

    def check_position(self, x):
        if x >= self.Mountain_pos[0]:
            return self.T_amb2, self.wind, self.gamma, True
        else:
            return self.T_amb, self.wind2, self.gamma2, False

    def Sampling(self):

        for drone in self.UAVs:
            (T, w, wind_angle, flag_pos) = self.check_position(drone.x)
            # Time_stamp, id_drone, T_amb, wind, gamma, position_x, position_y, speed, battery, actual consumption, distance, bitrate, 'pkt lost tot', 'pkt lost missing', 'pkt lost iteration'
            new_row = [self.sim_time, drone.id, T, self.T_amb2, self.T_amb, w, wind_angle * 180 / math.pi, drone.x,
                       drone.y, drone.mod_v_real,
                       drone.Ej / self.Initial_Ej * 100, drone.act_cons / 3600, drone.distance, drone.distance_GS,
                       drone.bitrate / 1e6, 0, 0, 0, 0]
            # drone.pkt_lost_tot, drone.pkt_lost_image_missing, drone.pkt_lost_iteration, drone.pkt_lost_json]

            # some elements are list??
            for i in range(0, len(new_row)):
                if isinstance(new_row[i], np.ndarray):
                    new_row[i] = new_row[i].item()

            self.df.loc[len(self.df)] = new_row

        # schedule a new event
        self.count_Sample_Time += 1
        self.FES.add_events(self.count_Sample_Time * self.T_sample, "Sampling", -1)

    def graphs(self):

        if self.FLAG_graphs:
            # print(df.head())
            self.df.to_csv('Simulation_result.csv')  # uncomment to save the data in a csv file

            # df = pd.read_csv('Simulation_result.csv')

            name_fig = ['T_amb', 'wind_speed', 'wind_angle', 'position_x', 'position_y', 'UAV_speed', 'battery_level',
                        'actual_consumption', 'waypoint_distance', 'distance_from_GS', 'bitrate',
                        'pkt_lost_tot']  # , 'pkt_lost_image_missing', 'pkt_lost_iteration']

            df_ = self.df.copy()
            # df_pkt_lost = df_[['Time_stamp [s]', 'id_drone', 'pkt lost tot', 'pkt lost missing', 'pkt lost iteration','pkt lost old']]
            # name_pkt_lost = ['pkt_lost_tot', 'pkt_lost_missing', 'pkt_lost_iteration']
            df_temp = df_[['Time_stamp [s]', 'id_drone', 'T_amb [°C]', 'T-right', 'T-left']]

            df_ = df_.drop(['pkt lost missing', 'pkt lost iteration', 'pkt lost old', 'T-right', 'T-left'], axis=1)
            columns_ = df_.columns[2:]

            # graphs of temperature
            x = df_temp['id_drone'].unique()
            time_autonomy = []

            for id_drone in x:
                df_drone = df_temp[df_temp['id_drone'] == id_drone]
                time_autonomy.append(df_drone['Time_stamp [s]'].iloc[-1])

            f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))

            ax1.stem(x, time_autonomy, linefmt='b-', markerfmt='bo', basefmt='-')

            # Titoli e etichette degli assi
            ax1.set_ylim([min(time_autonomy) - 10, max(time_autonomy) + 10])
            ax1.set_title('Time Duration per each UAV')
            ax1.set_xlabel('ID drone')
            ax1.set_ylabel('Time Availability [s]')
            ax1.grid(True)

            # Temperature per each UAV
            T_mean = df_temp.groupby('id_drone').agg({'T_amb [°C]': ['mean']})

            for id_drone in x:
                ax2.plot([id_drone, id_drone],
                         [min((T_mean.to_numpy()).flatten()) - 1, T_mean.loc[:, ('T_amb [°C]', 'mean')][id_drone]],
                         color='b')
            ax2.scatter(x, T_mean.loc[:, ('T_amb [°C]', 'mean')], color='b')

            # Titoli e etichette degli assi
            ax2.set_ylim([min((T_mean.to_numpy()).flatten()) - 1, max((T_mean.to_numpy()).flatten()) / 2])
            # ax2.set_legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax2.set_title('Average Temperature per each UAV')
            ax2.set_xlabel('ID drone')
            ax2.set_ylabel('Temperature [°C]')
            ax2.grid(True)

            plt.subplots_adjust(hspace=0.5)
            # plt.show()

            if FLAG_OS == 'Windows':
                filename = "figures" + "\\" + "UAVs_statistics" + ".png"
            elif FLAG_OS == 'MAC':
                filename = "figures/" + "time_duration" + ".png"

            plt.savefig(filename, bbox_inches='tight')

            if self.N_UAV <= 3:

                IDs = df_['id_drone'].unique()

                color = ['blue', 'green', 'red']
                color_map = {id: c for id, c in zip(IDs, color)}

                i = 0  # for the figures
                for col in columns_:
                    fig = plt.figure(figsize=(20, 10))
                    fig.canvas.required_interactive_framework = 'qt5'
                    for id in IDs:  # one curve per UAV

                        sub_df = df_[df_['id_drone'] == id]
                        x = sub_df['Time_stamp [s]'].unique()
                        plt.plot(x, sub_df[col].to_numpy(), marker='s', markersize=2, color=color_map[id],
                                 label=("drone " + str(int(id))))

                    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                    plt.ylabel(col)
                    plt.xlabel('Time [s]')
                    plt.grid()

                    if FLAG_OS == 'Windows':
                        filename = "figures" + "\\" + name_fig[i] + ".png"
                    elif FLAG_OS == 'MAC':
                        filename = "figures/" + name_fig[i] + ".png"

                    plt.savefig(filename, bbox_inches='tight')
                    plt.close()
                    i += 1
            else:
                # first UAV and last one to stop
                a = df_['id_drone'].value_counts().reset_index()
                first_drone_to_stop = df_[df_['id_drone'] == int(a.iloc[-1][0])]
                last_drone_to_stop = df_[df_['id_drone'] == int(a.iloc[0][0])]

                first_time_to_stop = first_drone_to_stop['Time_stamp [s]'].to_numpy()[-1]
                last_time_to_stop = last_drone_to_stop['Time_stamp [s]'].to_numpy()[-1]

                # min, max, mean
                df_min_max_mean = df_.drop(['id_drone'], axis=1).groupby(['Time_stamp [s]']).agg(['min', 'max', 'mean'])
                legend_names = [' min', ' max', ' mean']
                title_names = df_.columns[2:]
                list_name = []
                for col in df_.columns[2:]:
                    for col2 in [' min', ' max', ' mean']:
                        list_name.append(col + col2)

                df_min_max_mean.columns = list_name

                # calculate mean and standard deviation for each variable
                df_mean_std = df_.drop(['id_drone'], axis=1).groupby(['Time_stamp [s]']).agg(['mean', 'std'])

                x = df_['Time_stamp [s]'].unique()

                i = 0  # for the figures
                j = 0  # for the image saving
                for col in list_name:

                    if i == 3 or i == 0:
                        fig = plt.figure(figsize=(20, 10))
                        fig.canvas.required_interactive_framework = 'qt5'
                        i = 0

                    # plot min, max, and mean values
                    plt.plot(x, df_min_max_mean[col].to_numpy(), marker='s', markersize=2, label=legend_names[i])
                    i += 1

                    if i == 3:
                        # calculate mean and standard deviation for the current variable
                        sample_mean = df_mean_std.loc[:, (title_names[j], "mean")].to_numpy()
                        sample_std = df_mean_std.loc[:, (title_names[j], "std")].to_numpy()

                        # calculate confidence interval
                        if columns_[j] in ['UAV speed [m/s]', 'battery level [%]', 'bitrate [Mbps]', 'pkt lost tot',
                                           'pkt lost missing', 'pkt lost iteration', 'pkt lost old']:
                            if self.N_UAV < 30:  # t-student distribution
                                #       print("t-distribution distribution", self.N_UAV)
                                lower, upper = t.interval(0.95, self.N_UAV - 1, loc=sample_mean,
                                                          scale=sample_std / np.sqrt(self.N_UAV))
                            else:  # normal distribution
                                #      print("normal distribution", self.N_UAV)
                                z_value = norm.ppf(0.975)  # for 95% confidence interval
                                lower = sample_mean - z_value * sample_std / np.sqrt(self.N_UAV)
                                upper = sample_mean + z_value * sample_std / np.sqrt(self.N_UAV)

                            # plot the confidence interval
                            plt.fill_between(x, lower, upper, interpolate=True, alpha=0.2, color='blue',
                                             label='confidence interval')

                        # end of simulation
                        plt.axvline(first_time_to_stop, color='k', linestyle='--',
                                    label='first drone runs out of energy')
                        plt.axvline(last_time_to_stop, color='gray', linestyle='--', label='end of simulation')

                        plt.ylabel(title_names[j])
                        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                        plt.xlabel('Time [s]')
                        plt.grid()

                        if FLAG_OS == 'Windows':
                            filename = "figures" + "\\" + name_fig[j] + ".png"
                        elif FLAG_OS == 'MAC':
                            filename = "figures/" + name_fig[i] + ".png"

                        plt.savefig(filename, bbox_inches='tight')

                        # filename = "figures" + "\\" + name_fig[j] + ".png"

                        plt.close()

                        # first UAV and last one to stop
                        fig = plt.figure(figsize=(20, 10))
                        fig.canvas.required_interactive_framework = 'qt5'

                        if columns_[j] == 'battery level [%]':

                            x_ = first_drone_to_stop['Time_stamp [s]'].unique()
                            plt.plot(x_, first_drone_to_stop[columns_[j]].to_numpy(), linestyle="None", color="black",
                                     marker='s', markersize=3, label=("First UAV runs out of energy"))

                            x_ = last_drone_to_stop['Time_stamp [s]'].unique()
                            plt.plot(x_, last_drone_to_stop[columns_[j]].to_numpy(), linestyle="--", color="red",
                                     marker='s', markersize=3, label=("Last UAV runs out of energy"))

                            plt.plot(x, df_min_max_mean[col].to_numpy(), marker='s', markersize=2, label='mean')
                            plt.fill_between(x, lower, upper, interpolate=True, alpha=0.2, color='blue',
                                             label='confidence interval')

                            plt.title("UAVs battery levels")
                            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                            plt.ylabel(title_names[j])

                        elif columns_[j] == 'bitrate [Mbps]':
                            x_ = first_drone_to_stop['Time_stamp [s]'].unique()
                            plt.plot(x_, first_drone_to_stop[columns_[j]].to_numpy(), linestyle="None", color="black",
                                     marker='s', markersize=3, label=("First UAV runs out of energy"))

                            x_ = last_drone_to_stop['Time_stamp [s]'].unique()
                            plt.plot(x_, last_drone_to_stop[columns_[j]].to_numpy(), linestyle="None", color="red",
                                     marker='s', markersize=3, label=("Last UAV runs out of energy"))

                            plt.title("UAVs battery levels")
                            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                            plt.ylabel(title_names[j])
                        else:

                            x_ = first_drone_to_stop['Time_stamp [s]'].unique()
                            plt.plot(x_, first_drone_to_stop[columns_[j]].to_numpy(), linestyle="--", color="black",
                                     marker='s', markersize=3, label=("First UAV runs out of energy"))

                            x_ = last_drone_to_stop['Time_stamp [s]'].unique()
                            plt.plot(x_, last_drone_to_stop[columns_[j]].to_numpy(), linestyle="--", color="red",
                                     marker='s', markersize=3, label=("Last UAV runs out of energy"))

                            plt.title("First UAV and Last one to stop")
                            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                            plt.ylabel(title_names[j])

                        plt.xlabel('Time [s]')
                        plt.grid()

                        if FLAG_OS == 'Windows':
                            filename = "figures" + "\\" + name_fig[j] + "First_End.png"
                        elif FLAG_OS == 'MAC':
                            filename = "figures/" + name_fig[i] + ".png"

                        plt.savefig(filename, bbox_inches='tight')
                        plt.close()

                        j += 1

            self.FLAG_graphs = False

    def text_controller(self, screen):

        # font
        font = pygame.font.SysFont('Courier', 20, bold=True, italic=False)
        green_blue = (0, 255, 0)
        red = (255, 0, 0)

        X1 = self.SCREEN_WIDTH / 4 + 45
        X2 = 3 / 4 * self.SCREEN_WIDTH + 25

        wind_color = round(255 - 255 * self.wind / 10)
        wind_color2 = round(255 - 255 * self.wind2 / self.max_wind)

        # LEFT PART OF THE SCREEN
        text_surface_1 = font.render('Temperature left: %.1f°C' % (self.T_amb), True, [255, 200, 0])

        text_surface_2 = font.render('Wind speed left: %.2f m/s, %.0f°' % (self.wind2, self.gamma2 * 180 / math.pi),
                                     True,
                                     [255, wind_color2, 0])

        Text_width = max(text_surface_1.get_width() + 40, text_surface_2.get_width() + 40)
        X1 -= Text_width / 2

        screen.blit(text_surface_1, (X1, 105))
        screen.blit(text_surface_2, (X1, 110 + text_surface_2.get_height() + 2))

        # RIGHT PART OF THE SCREEN
        text_surface_1 = font.render('Temperature right: %.1f°C' % (self.T_amb2), True, [255, 200, 255])

        text_surface_2 = font.render('Wind speed right: %.2f m/s, %.0f°' % (self.wind, self.gamma * 180 / math.pi),
                                     True, [255, wind_color, 255])

        Text_width = max(text_surface_1.get_width() + 40, text_surface_2.get_width() + 40)
        X2 -= Text_width / 2

        screen.blit(text_surface_1, (X2, 105))
        screen.blit(text_surface_2, (X2, 110 + text_surface_2.get_height() + 2))

        # Simulation time

        min = np.floor(self.sim_time / 60)
        sec = np.floor(self.sim_time % 60)
        cent = (self.sim_time - (min * 60 + sec))

        text_surface = font.render('Simulation Time: %d min %d.%d s' % (min, sec, cent), True, [255, 255, 255])
        X = self.SCREEN_WIDTH - text_surface.get_width() - 25
        Y = self.HEIGHT_controller - 35
        screen.blit(text_surface, (X, Y))

        if N_missing > 0:
            text_surface = font.render(
                'MISSING PERSON --> (%.2f, %.2f)m' % (self.coord_disperso[0][0], self.coord_disperso[0][1]), True, red)
            screen.blit(text_surface, (X2, 35))

    def rotatePolygon(self, polygon, theta, WP_x, WP_w, WP_y, WP_h):
        """Rotates the given polygon which consists of corners represented as (x,y), around the ORIGIN, clock-wise, theta degrees"""
        rotatedPolygon = []
        center = (WP_x + WP_w / 2, WP_y + WP_h / 2)
        for corner in polygon:
            rotatedPolygon.append(
                ((corner[0] - center[0]) * math.cos(theta) - (corner[1] - center[1]) * math.sin(theta) + center[0],
                 (corner[0] - center[0]) * math.sin(theta) + (corner[1] - center[1]) * math.cos(theta) + center[1]))
        return rotatedPolygon



if __name__ == "__main__":
    seed = 4

    S = Simulation(seed)
    S.Start()
