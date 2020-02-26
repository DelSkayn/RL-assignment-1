from .player import Player
from hex_skeleton import HexBoard
import math

class AlphaBeta(Player):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.depth = 3
        self.other_color = HexBoard.RED
        if self.color == HexBoard.RED:
            self.other_color = HexBoard.BLUE

    def name():
        return "Alpha Beta Base"

    def eval(self, board, maxi):
        if board.is_game_over():
            if maxi:
                return -math.inf
            else:
                return math.inf
        return 0

    def get_nodes(board):
        for i in range(board.size):
            for j in range(board.size):
                if board.is_empty((i,j)):
                    yield (i,j)

    def alpha_beta(self, board, depth, alpha, beta, maxi):
        self.nodes_searched += 1;
        if depth == 0 or board.is_game_over():
            return self.eval(board,maxi)
        if maxi:
            value = -math.inf
            for node in AlphaBeta.get_nodes(board):
                board.place(node,self.color)
                n_value = self.alpha_beta(board, depth-1, alpha,beta,False)
                board.undo_place(node)
                value = max(value,n_value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for node in AlphaBeta.get_nodes(board):
                board.place(node,self.other_color)
                n_value = self.alpha_beta(board, depth-1, alpha, beta, True)
                board.undo_place(node)
                value = min(value,n_value)
                beta = min(beta,value)
                if alpha >= beta:
                    break
            return value

    def make_move(self,board):
        best = -math.inf
        best_moves = []
        self.nodes_searched = 0
        for node in AlphaBeta.get_nodes(board):
            board.place(node,self.color)
            self.nodes_searched += 1;
            value = self.alpha_beta(board,self.depth, best, math.inf, False)
            self.nodes_searched += 1;
            board.undo_place(node)
            if value == best:
                best_moves.append(node)
            elif value > best:
                best = value
                best_moves = [node]
        best_move = self.random.choice(best_moves)
        board.place(best_move,self.color)

export = AlphaBeta
