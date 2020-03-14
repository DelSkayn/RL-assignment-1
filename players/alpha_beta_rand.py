from .alpha_beta import AlphaBeta

# Alpha beta but with a random evaluation function
class AlphaBetaRandom(AlphaBeta):

    def name():
        return "Alpha Beta Random"

    def eval(self, board, maxi):
        return self.random.randint(-self.max_value,self.max_value)

export = AlphaBetaRandom
