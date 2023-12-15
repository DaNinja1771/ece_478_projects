import math
import numpy as np
from queue import Queue
from enum import Enum

class State(Enum):
    idle                = 0
    ready_to_transmit   = 1
    waiting_to_transmit = 2
    transmitting        = 3
    sending_RTS         = 4
    waiting_NAV         = 5

class Node:

    def __init__(self, sim_params, frame_rate, seed=None):
        np.random.seed(seed)
        self.ack = sim_params.ACK_dur
        self.backoff = None
        self.difs_duration = sim_params.DIFS_dur
        self.cw_0 = sim_params.CW_0
        self.cw_max = sim_params.CW_max
        self.cw = self.cw_0
        self.sifs_duration = sim_params.SIFS_dur
        self.frame_distribution = self.gen_dist(frame_rate,
                                           sim_params.max_sim_time_sec)
        self.frame_idx = 0
        self.state = State.idle
        self.queue = Queue(maxsize=len(self.frame_distribution))
        self.transmit_count = 0
        self.valid = True
        self.RTS_end = 0
        self.NAV = 0
        self.CTS_count = 0


    def check_packet_ready(self, slot, otherNode):
        if slot == self.frame_distribution[self.frame_idx]:
            self.queue.put(slot)
            if self.frame_idx < len(self.frame_distribution) - 1:
                self.frame_idx += 1 
        if self.state == State.transmitting:
            return
        elif not self.queue.empty() and not (self.state == State.waiting_to_transmit or self.state == State.sending_RTS) and not otherNode.transmit_count >1:
            self.state = State.ready_to_transmit


    def calc_backoff(self):
        temp_cw = min(self.cw, self.cw_max)
        self.backoff = np.random.randint(0, temp_cw-1)
        
        
    def gen_dist(self, lam, t, t_slot=10e-6):
        u = np.random.uniform(size=(lam*t))
        x = [-(1/lam) * math.log(1-i) for i in u]
        x = [math.ceil(i/t_slot) for i in x]
        x = list(np.cumsum(x))
        return x
    
    def get_transmit_count(self, sim_params):
        return sim_params.frame_size_slots + sim_params.SIFS_dur + sim_params.ACK_dur
    def get_NAV(self, sim_params):
        return 2 + sim_params.SIFS_dur + 2 + sim_params.SIFS_dur + self.get_transmit_count(sim_params)
    
    def collision(self):
        self.state = State.idle
        self.cw = self.cw * 2
        self.backoff = None
        self.difs_duration = 2
        self.valid = True
    
    def reset_node(self):
        self.cw = self.cw_0
        self.state = State.idle
        self.difs_duration = 2
        self.backoff = None
        self.valid = True