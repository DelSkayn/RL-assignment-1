from .monte_carlo import MonteCarlo
from hex_skeleton import HexBoard
import copy

# monte carlo with different amount of random games
class MonteCarlo100(MonteCarlo):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.num_tries = 100

    def name():
        return "MonteCarlo 100"

#export = MonteCarlo100
