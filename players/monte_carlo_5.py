from .monte_carlo import MonteCarlo
from hex_skeleton import HexBoard
import copy

class MonteCarlo5(MonteCarlo):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.num_tries = 5

    def name(self):
        return "MonteCarlo 5"

export = MonteCarlo5
