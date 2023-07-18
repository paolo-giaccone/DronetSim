import math

class clouds:
    def __init__(self, init_x, init_y, SCREEN_WIDTH, SCREEN_HEIGH):
        self.cloud_x = init_x
        self.cloud_y = init_y
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGH = SCREEN_HEIGH
        self.distance_C_GS = 0

    def cloud_motion(self, delta_t, gs_x, gs_y, SCALE_FACTOR, wind_speed, wind_angle, r, type_object):
        dx = delta_t * wind_speed * math.cos(wind_angle)/1e1
        dy = delta_t * wind_speed * math.sin(wind_angle)/1e1
        self.cloud_x += dx
        self.cloud_x = self.cloud_x % (self.SCREEN_WIDTH + 160)
        self.cloud_y += dy
        self.cloud_y = self.cloud_y % self.SCREEN_HEIGH
        # distance between mountain and cloud
        self.distance_C_GS = math.sqrt((self.cloud_x - gs_x) ** 2 + (self.cloud_y - gs_y) ** 2) * SCALE_FACTOR




