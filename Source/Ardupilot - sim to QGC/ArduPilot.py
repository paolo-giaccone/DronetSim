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


from pymavlink import mavutil
import pandas as pd
import time as tm
import math


def calculate_desired_yaw(current_x, current_y, target_x, target_y):
    # Calculate the difference in x and y coordinates
    diff_x = target_x - current_x
    diff_y = target_y - current_y
    # Calculate the desired yaw angle using atan2
    desired_yaw = math.atan2(diff_x, diff_y) + math.pi / 2
    # Ensure that the angle is within the range of 0 to 2*pi
    if desired_yaw < 0:
        desired_yaw += 2 * math.pi

    return desired_yaw


Waypoint = pd.read_csv('Waypoints_first_UAV')

# Create the connection
the_connection = mavutil.mavlink_connection('udpin:localhost:14550')
# Wait a heartbeat before sending commands
the_connection.wait_heartbeat()
print(
    "Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

# ARM
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

# wait until arming confirmed (can manually check with master.motors_armed())
print("Waiting for the vehicle to arm")
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print('Armed!')
print(msg)

# TAKEOFF
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)

print('TAKE OFF')
msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

the_connection.close()
tm.sleep(10 / 2.5 + 5)
print('TAKE OFF Completed')
# movement
cnt = 0
while cnt < Waypoint.shape[0]:
    print('Waypoint n°', str(cnt + 1))
    Waypoint_x = Waypoint.iloc[cnt, 1]
    Waypoint_y = Waypoint.iloc[cnt, 2]
    if cnt != 0:
        desired_yaw = calculate_desired_yaw(Waypoint.iloc[cnt - 1, 1], Waypoint.iloc[cnt - 1, 2], Waypoint_x,
                                            Waypoint_y)
    else:
        desired_yaw = calculate_desired_yaw(0, 0, Waypoint_x, Waypoint_y)
    print(desired_yaw, type(desired_yaw))

    # third position of Waypoint dataframe corresponds to the module of the velocity
    v_x = abs(Waypoint.iloc[cnt, 3] * math.cos(desired_yaw))
    v_y = abs(Waypoint.iloc[cnt, 3] * math.sin(desired_yaw))
    print(v_x, v_y)

    # Start a connection listening on a UDP port
    the_connection = mavutil.mavlink_connection('udpin:localhost:14550')  # tcp:127.0.0.1:5760

    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (
    the_connection.target_system, the_connection.target_component))

    the_connection.mav.send(
        mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                                                                      the_connection.target_component,
                                                                      mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                                                                      int(0b110111000000), Waypoint_x, Waypoint_y, -100,
                                                                      v_x, v_y, 0, 0, 0, 0, desired_yaw, 0))
    # message SET_POSITION_TARGET_LOCAL_NED 0 0 0 1 3527 0 0 0 1 0 0 0 0 0 0 0
    the_connection.close()
    # msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
    # print(msg)
    if cnt != 0:
        dist = math.sqrt((Waypoint.iloc[cnt, 1] - Waypoint.iloc[cnt - 1, 1]) ** 2 + (
                    Waypoint.iloc[cnt, 2] - Waypoint.iloc[cnt - 1, 2]) ** 2)
    else:
        dist = math.sqrt((Waypoint.iloc[cnt, 1]) ** 2 + (Waypoint.iloc[cnt, 2]) ** 2)

    tm.sleep(dist / 10)

    cnt += 1