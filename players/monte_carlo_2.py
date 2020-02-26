from .monte_carlo import MonteCarlo
from hex_skeleton import HexBoard
import copy

class MonteCarlo2(MonteCarlo):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.num_tries = 2

    def name():
        return "MonteCarlo 2"

#export = MonteCarlo2
