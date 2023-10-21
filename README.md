# DronetSim 

The repository provides a UAV simulator developed with the course "Project: Software-Defined Communications Systems" of MSc in Communications Engineer during the academic year 2022-23 by Andrea Cuzzi, Loredana Logruosso, Luca Nepote, supervised by prof. Paolo Giaccone and Dr. Francesco Raviglione.

The work has been motivated by __Flagship project__ **Space4You** within **NODES** project, which has received funding from the __MUR – Missione 4__, Componente 2, Investimento 1.5 – Creazione e rafforzamento di “**Ecosistemi dell’innovazione**”, costruzione di “leader territoriali di R&S” – del PNRR with grant agreement no. ECS00000036.

The UAV simulator is aimed at investigating a basic scenario in which generic airborn vehicles move in a given area and communicate within a multihop fashion. The simulation model captures many aspects:
- flexible communication model
- packet transmission modeling
- temperature effects on battery duration
- environment effects on the mobility (e.g., wind)
- cooperative multihop communication between UAV

A GUI is provided to show in real time the currect state of the simulation.

DronetSim is also integrated with Ardupilot.

The main assumptions behind the simulation model are the following:
- ideal MAC, i.e., no collisions
- no queueing on the relay nodes

## Folder structure

- Source: DronetSim python code
- Doc: Main documentation, with manual and report showing some simulation results under some meaningful scenarios
- Script: auxiliary files to process the simulation output  
