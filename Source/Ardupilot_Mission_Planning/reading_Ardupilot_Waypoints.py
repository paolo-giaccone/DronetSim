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


import pandas as pd
import numpy as np
from math import radians, sin, cos, acos, pi
from geopy.distance import geodesic
from geopy import Point

  
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading the file.")

# Esempio di utilizzo
file_path = './mission.txt'
file_content = read_text_file(file_path)
lines = file_content.split('\n')

Waypoint = pd.DataFrame(columns=['latitude','longitude'])
for i, line in enumerate(lines):
    line_list = line.split('\t')
    if i != 0:
        new_row = {'latitude':float(line_list[-7]),'longitude':float(line_list[-5])}
        Waypoint = Waypoint._append(new_row, ignore_index=True)


# Elimina le righe con solo valori zero (0.0000)
Waypoint = Waypoint.loc[~(Waypoint == 0.000000).all(axis=1)]
Waypoint.reset_index(drop=True, inplace=True)

# Convertire Latitudine e Longitudine in distanza
Waypoint_distance = pd.DataFrame(columns = ['x','y'])
start_pos = Waypoint.iloc[0].to_numpy()
lat_in = start_pos[0]
long_in = start_pos[1]
point_in = Point(lat_in,long_in)

for i in range(1,Waypoint.shape[0]):
    
    currest_pos = Waypoint.iloc[i].to_numpy()
    lat_last = currest_pos[0]
    long_last = currest_pos[1]

    point1 = Point(lat_in, long_last)
    y = geodesic(point_in, point1).meters

    point2 = Point(lat_last, long_in)
    x = geodesic(point_in, point2).meters

    new_row = {'x':x,'y':y}
    Waypoint_distance = Waypoint_distance._append(new_row, ignore_index = True)



    
Waypoint.to_csv('Ardupilot Mission Plan')
Waypoint_distance.to_csv('Ardupilot Waypoints')