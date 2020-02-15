from .monte_carlo import MonteCarlo
from hex_skeleton import HexBoard
import copy

class MonteCarlo20(MonteCarlo):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.num_tries = 10

    def name(self):
        return "MonteCarlo 20"

export = MonteCarlo20
