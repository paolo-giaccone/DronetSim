import math

class clouds:
    def __init__(self, init_x, init_y, SCREEN_WIDTH, SCREEN_HEIGH):
        # cloud position
        self.cloud_x = init_x
        self.cloud_y = init_y
        # dimensions of the map
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGH = SCREEN_HEIGH
        # distance wrt the ground station
        self.distance_C_GS = 0

    # motion of the clouds according to the wind
    def cloud_motion(self, delta_t, gs_x, gs_y, SCALE_FACTOR, wind_speed, wind_angle):
        # increments on the x and y positions, according to the wind
        dx = delta_t * wind_speed * math.cos(wind_angle)/1e1
        dy = delta_t * wind_speed * math.sin(wind_angle)/1e1
        # updating of the position and checking if they go out from the map
        self.cloud_x += dx
        self.cloud_x = self.cloud_x % (self.SCREEN_WIDTH + 160)
        self.cloud_y += dy
        self.cloud_y = self.cloud_y % self.SCREEN_HEIGH
        # updating the distance between ground station and cloud
        self.distance_C_GS = math.sqrt((self.cloud_x - gs_x) ** 2 + (self.cloud_y - gs_y) ** 2) * SCALE_FACTOR




