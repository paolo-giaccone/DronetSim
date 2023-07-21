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


import tkinter as tk
import math

class Parameter_Initialization():
    def __init__(self, max_wind):
        # Parameter Initialization #
        self.ardupilot_flag = False
        # False: random waypoints / True: ardupilot waypoints
        self.settings = False
        # settings: the simulation starts when there are correct parameters set
        self.max_wind = max_wind # to compare the inserted value

        # generation of the parameters window
        self.window = tk.Tk()
        self.window.geometry("900x820")
        self.window.resizable(False, False)
        self.window.configure(background="white")
        self.window.title("Parameter Initialization")

        # Header Environmental Parameters
        self.Separation_EE = tk.Label(self.window, text="Environmental Parameters",
                                   pady=5, padx=5, font=("Helvetica", 20))
        self.Separation_EE.grid(row=0, columnspan=4, sticky="WE", padx=10, pady=10)

        ## FIRST PART
        # initial temperature
        self.welcome_label = tk.Label(self.window, text="Initial Temperature 1 [°C]:",
                                 pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label.grid(row=1, column=0, sticky="WE", padx=10, pady=10)

        # definition of T_in
        self.text_input = tk.Entry()
        self.text_input.grid(row=1, column=1, sticky="WE", pady=10, padx=5)

        # Wind velocity
        self.welcome_label_2 = tk.Label(self.window, text="Initial Wind Velocity 1 [m/s]:",
                                   pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_2.grid(row=2, column=0, sticky="WE", padx=10, pady=10)

        # definition of wind velocity
        self.text_input_2 = tk.Entry()
        self.text_input_2.grid(row=2, column=1, sticky="WE", pady=10, padx=10)

        # Wind Angle
        self.welcome_label_3 = tk.Label(self.window, text="Wind Angle 1 [°]:",
                                   pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_3.grid(row=3, column=0, sticky="WE", padx=10, pady=10)

        # definition of wind velocity
        self.text_input_3 = tk.Entry()
        self.text_input_3.grid(row=3, column=1, sticky="WE", pady=10, padx=10)


        ## SECOND PART
        # initial temperature
        self.welcome_label_4 = tk.Label(self.window, text="Initial Temperature 2 [°C]:",
                                      pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_4.grid(row=1, column=2, sticky="WE", padx=10, pady=10)

        # definition of T_in
        self.text_input_4 = tk.Entry()
        self.text_input_4.grid(row=1, column=3, sticky="WE", pady=10, padx=5)

        # Wind velocity
        self.welcome_label_5 = tk.Label(self.window, text="Initial Wind Velocity 2 [m/s]:",
                                        pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_5.grid(row=2, column=2, sticky="WE", padx=10, pady=10)

        # definition of wind velocity
        self.text_input_5 = tk.Entry()
        self.text_input_5.grid(row=2, column=3, sticky="WE", pady=10, padx=10)

        # Wind Angle
        self.welcome_label_6 = tk.Label(self.window, text="Wind Angle 2 [°]:",
                                        pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_6.grid(row=3, column=2, sticky="WE", padx=10, pady=10)

        # definition of wind velocity
        self.text_input_6 = tk.Entry()
        self.text_input_6.grid(row=3, column=3, sticky="WE", pady=10, padx=10)

        ## SIMULATION PARAMETERS
        # Header Simulation Parameters
        self.Separation = tk.Label(self.window, text="Simulation Parameters",
                                        pady=5, padx=5, font=("Helvetica", 20))
        self.Separation.grid(row=4, columnspan=4, sticky="WE",  padx=10, pady=10)

        # definition of number of UAVs
        self.welcome_label_7 = tk.Label(self.window, text="Number of UAVs:",
                                   pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_7.grid(row=5, column=0, sticky="WE", padx=10, pady=10)

        self.text_input_7 = tk.Entry()
        self.text_input_7.grid(row=5, column=1, sticky="WE", pady=10, padx=10)

        # Number of missing people
        self.welcome_label_8 = tk.Label(self.window, text="Number of Missing People:",
                                      pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_8.grid(row=6, column=0, sticky="WE", padx=10, pady=10)

        self.text_input_8 = tk.Entry()
        self.text_input_8.grid(row=6, column=1, sticky="WE", pady=10, padx=10)

        # Number of clouds
        self.welcome_label_9 = tk.Label(self.window, text="Number of Clouds:",
                                        pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_9.grid(row=7, column=0, sticky="WE", padx=10, pady=10)

        self.text_input_9 = tk.Entry()
        self.text_input_9.grid(row=7, column=1, sticky="WE", pady=10, padx=10)

        ## COMMUNICATION PARAMETERS
        # definition of the Length of the Queue
        self.welcome_label_10 = tk.Label(self.window, text="Length of the Queue:",
                                        pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_10.grid(row=5, column=2, sticky="WE", padx=10, pady=10)

        self.text_input_10 = tk.Entry()
        self.text_input_10.grid(row=5, column=3, sticky="WE", pady=10, padx=10)

        # N° Retrx Attempts, Low Priority
        self.welcome_label_11 = tk.Label(self.window, text="N° Retrx Attempts, Low Priority:",
                                        pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_11.grid(row=6, column=2, sticky="WE", padx=10, pady=10)

        self.text_input_11 = tk.Entry()
        self.text_input_11.grid(row=6, column=3, sticky="WE", pady=10, padx=10)

        # N° Retrx Attempts, high Priority
        self.welcome_label_12 = tk.Label(self.window, text="N° Retrx Attempts, High Priority:",
                                         pady=5, padx=5, font=("Helvetica", 15))
        self.welcome_label_12.grid(row=7, column=2, sticky="WE", padx=10, pady=10)

        self.text_input_12 = tk.Entry()
        self.text_input_12.grid(row=7, column=3, sticky="WE", pady=10, padx=10)

        # ArduPilot
        self.Ardupilot = tk.Button(text="Ardupilot", command=self.Ardupilot, width=len("Ardupilot"), font=("Helvetica", 15))
        self.Ardupilot.grid(row=8, columnspan=2, sticky="WE", pady=10, padx=10)

        # button for initialization
        self.T_button = tk.Button(text="Initialize", command=self.initialize, width=len("Initialize"), font=("Helvetica", 15))
        self.T_button.grid(row=8, column=2, columnspan=2, sticky="WE", pady=10, padx=10)

        self.start_button = tk.Button(text="Start", command=self.start_simulation, width=len("Start"),font=("Helvetica", 15))
        self.start_button.grid(row=9, columnspan=4, sticky="WE", pady=10, padx=10)

        self.window.mainloop()

    ## INITIALIZE BUTTON

    def initialize(self):
        # in order to see if all the parameters have been set up correctly
        if (self.text_input.get() and self.text_input_2.get() and self.text_input_3.get() and self.text_input_4.get() and self.text_input_5.get() and
            self.text_input_6.get() and self.text_input_7.get() and self.text_input_8.get() and self.text_input_9.get() and self.text_input_10.get() and self.text_input_11.get() and self.text_input_12.get()):
            if not -20 <= int(self.text_input.get()) <= 40:
                text_response = (
                            "Temperature 1 input value must be in the range [-20,40]! \nActual given value: %d°C" % int(
                        self.text_input.get()))
            elif not 0 <= int(self.text_input_2.get()) <= self.max_wind:  # decidere che valore limite del vento mettere
                text_response = ("Wind value 1 must be in the range [0,10]! \nActual given value: %d m/s" % int(
                    self.text_input_2.get()))
            elif not 0 <= int(self.text_input_3.get()) <= 360:
                text_response = ("Wind angle 1 value must be in the range [0,360]! \nActual given value: %d°" % int(
                    self.text_input_3.get()))
            elif not -20 <= int(self.text_input_4.get()) <= 40:
                text_response = (
                            "Temperature 2 input value must be in the range [-20,40]! \nActual given value: %d°C" % int(
                        self.text_input_4.get()))
            elif not 0 <= int(self.text_input_5.get()) <= self.max_wind:  # decidere che valore limite del vento mettere
                text_response = ("Wind value 2 must be in the range [0,10]! \nActual given value: %d m/s" % int(
                    self.text_input_5.get()))
            elif not 0 <= int(self.text_input_6.get()) <= 360:
                text_response = ("Wind angle 2 value must be in the range [0,360]! \nActual given value: %d°" % int(
                    self.text_input_6.get()))
            elif not int(self.text_input_7.get()) > 0:
                text_response = ("UAVs number must be bigger than 0! \nActual given value: %d" % int(
                    self.text_input_7.get()))
            elif not int(self.text_input_8.get()) >= 0:
                text_response = ("Missing people number: Negative value not allowed! \nActual given value: %d" % int(
                    self.text_input_8.get()))
            elif not int(self.text_input_9.get()) >= 0:
                text_response = ("Clouds number: Negative value not allowed! \nActual given value: %d" % int(
                    self.text_input_9.get()))
            elif not int(self.text_input_10.get()) > 0:
                text_response = ("Queue Length: value must be bigger than 0! \nActual given value: %d" % int(
                    self.text_input_10.get()))
            elif not int(self.text_input_11.get()) >= 0:
                text_response = ("N° Retr Attempt, Low Priority: Negative value not allowed! \nActual given value: %d" % int(
                    self.text_input_11.get()))
            elif not int(self.text_input_12.get()) >= 0:
                text_response = ("N° Retr Attempt, High Priority: Negative value not allowed! \nActual given value: %d" % int(
                    self.text_input_12.get()))
            # if all the parameters have been correctly set up
            else:
                text_response = ("T_in 1 = %s°C \nWind 1 = %s m/s \nWind Angle 1 = %s° \nT_in 2 = %s°C \nWind 2 = %s m/s \nWind Angle 2 = %s° \nNumber of UAVs = %s \nNumber of missing people = %s \nNumber of clouds = %s \nQueue Length = %s \nN° Retr Attempt, Low Priority = %s \nN° Retr Attempt, High Priority = %s \nArdupilot = %s"  % (
                    self.text_input.get(), self.text_input_2.get(), self.text_input_3.get(),self.text_input_4.get(),
                    self.text_input_5.get(),self.text_input_6.get(), self.text_input_7.get(), self.text_input_8.get(), self.text_input_9.get(), self.text_input_10.get(), self.text_input_11.get(), self.text_input_12.get(), self.ardupilot_flag))
                self.T_in1 = int(self.text_input.get())
                self.wind1 = int(self.text_input_2.get())
                gamma1 = int(self.text_input_3.get())
                self.gamma1 = math.pi / 180 * gamma1
                self.T_in2 = int(self.text_input_4.get())
                self.wind2 = int(self.text_input_5.get())
                gamma2 = int(self.text_input_6.get())
                self.gamma2 = math.pi / 180 * gamma2
                self.settings = True  # to start simulation
                self.numb_UAVs = int(self.text_input_7.get())
                self.numb_missing = int(self.text_input_8.get())
                self.numb_clouds = int(self.text_input_9.get())
                self.Queue_Length = int(self.text_input_10.get())
                self.N_RetrAttemptLP = int(self.text_input_11.get())
                self.N_RetrAttemptHP = int(self.text_input_12.get())

                self.ardupilot = self.Ardupilot

        else: # if some parameters have not been set up
            text_response = "Initialize parameters!"

        textwidget = tk.Text()
        textwidget.insert(tk.END, text_response)
        textwidget.grid(row=11, columnspan=4, sticky="WE", padx=10)

    # START BUTTON
    def start_simulation(self):
        if self.settings:
            self.window.quit() #close the window and start the simulation
        else:
            text_response2 = "Parameters not available! \nPlease, insert correct values!" #error
            textwidget2 = tk.Text()
            textwidget2.insert(tk.END, text_response2)
            textwidget2.grid(row=11, columnspan=2, sticky="WE", padx=10)

    # ARDUPILOT BUTTON
    def Ardupilot(self):
        if self.ardupilot_flag == False:
            text_response3 = "Ardupilot = True"
            textwidget3 = tk.Text()
            textwidget3.insert(tk.END, text_response3)
            textwidget3.grid(row=11, columnspan=4, sticky="WE", padx=10)
            self.ardupilot_flag = True
        else:
            text_response3 = "Ardupilot = False"
            textwidget3 = tk.Text()
            textwidget3.insert(tk.END, text_response3)
            textwidget3.grid(row=11, columnspan=4, sticky="WE", padx=10)
            self.ardupilot_flag = False