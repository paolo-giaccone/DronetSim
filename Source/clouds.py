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




