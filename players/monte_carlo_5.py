from .monte_carlo import MonteCarlo

# monte carlo with different amount of random games
class MonteCarlo5(MonteCarlo):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.num_tries = 5

    def name():
        return "MonteCarlo 5"

export = MonteCarlo5
