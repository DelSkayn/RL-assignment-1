from .alpha_beta import AlphaBeta
from hex_skeleton import HexBoard
import math

# Alpha beta but with a random evaluation function
class AlphaBetaRandom(AlphaBeta):

    def name():
        return "Alpha Beta Random"

    def eval(self, board, maxi):
        return self.random.randint(-self.max_value,self.max_value)

    def get_nodes(board):
        for i in range(board.size):
            for j in range(board.size):
                if board.is_empty((i,j)):
                    yield (i,j)


export = AlphaBetaRandom
