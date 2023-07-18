import queue
import random
import copy

class FES_management:
    def __init__(self, SIZE_JSON, DELTA_t_MSG_TO_SENT, DELTA_t_ENV_CHANGE,  N_UAV):
        self.FES = queue.PriorityQueue()
        self.SIZE_JSON = SIZE_JSON
        self.N_UAV = N_UAV
        self.DELTA_t_MSG_TO_SENT = DELTA_t_MSG_TO_SENT
        self.DELTA_t_ENV_CHANGE = DELTA_t_ENV_CHANGE

    def FES_Initialization(self, sim_time):
        # initialize the first event about the mobility
        self.FES.put((sim_time, "Choice of the trajectory", -1))  # for all drone at start

        #initialize the periodic msgs events
        rnd_initial_time = []
        for i in range(1, self.N_UAV + 1):
            rnd_initial_time.append(random.uniform(self.SIZE_JSON*8 , self.SIZE_JSON * 8 * i) )#self.SIZE_JSON /1e2)

        # schedule synch. msg each of them is out of phase (the phase is random)
        for j in range(1, self.N_UAV + 1):
            self.FES.put((self.DELTA_t_MSG_TO_SENT + (rnd_initial_time[j - 1]), "Send Telemetry Data", j))



        # change the temperature and the speed each T_effect_change
        for i in range(self.DELTA_t_ENV_CHANGE, 3600, self.DELTA_t_ENV_CHANGE):
            self.FES.put((i, "Change environmental effects", -1))


        # samples event
        self.FES.put((sim_time, "Sampling", -1))

    def add_events(self, sim_time, event, identification):
        self.FES.put((sim_time, event, identification))

    def read_event(self):
        tuple_event = self.FES.get()
        return tuple_event

    def remove_events(self, id_UAV, event):
        # Crea una nuova coda di priorità vuota in cui copiare tutte le tuple tranne quelle relative all'id utente da eliminare
        nuova_fes = queue.PriorityQueue()

        # Itera sulla coda di priorità finché non è vuota
        while not self.FES.empty():
            tupla = self.FES.get()
            tempo, evento, id_UAV_tupla = tupla
            if event == 'all':
                if isinstance(id_UAV_tupla, tuple):
                    if evento != 'Received Data' and id_UAV in id_UAV_tupla:
                        continue
                else:
                    if evento != 'Received Data' and id_UAV_tupla == id_UAV:
                        continue
                nuova_fes.put(tupla)
            else:
                if isinstance(id_UAV_tupla, tuple):
                    if event == evento and id_UAV in id_UAV_tupla:
                        continue
                else:
                    if event == evento and id_UAV_tupla == id_UAV:
                        continue
                nuova_fes.put(tupla)
        # Restituisci la nuova lista senza gli eventi relativi all'id utente da eliminare
        self.FES = nuova_fes

    def print_FES(self):
        # Crea una copia temporanea della lista
        FES_copy = self.FES.queue.copy()

        # Stampa gli elementi senza rimuoverli
        for event in FES_copy:
            print(event)
