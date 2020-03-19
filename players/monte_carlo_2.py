from .monte_carlo import MonteCarlo

# monte carlo with different amount of random games
class MonteCarlo2(MonteCarlo):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.num_tries = 2

#export = MonteCarlo2
