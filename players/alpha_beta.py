from .player import Player
from hexboard import HexBoard
import math
import time

# The basic implementation of a alpha beta searcher

class AlphaBeta(Player):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.depth = 4
        self.other_color = HexBoard.RED
        if self.color == HexBoard.RED:
            self.other_color = HexBoard.BLUE

        self.max_value = board_size * board_size

    def name(self):
        return "Alpha Beta Base"

    def eval(self, board, maxi):
        if board.is_game_over():
            if maxi:
                return -self.max_value
            else:
                return self.max_value
        return 0

    def get_nodes(board):
        return board.get_available_moves()

    def alpha_beta(self, board, depth, alpha, beta, maxi):
        self.nodes_searched += 1;
        if depth == 0 or board.is_game_over():
            return self.eval(board,maxi)
        if maxi:
            value = -self.max_value
            for node in AlphaBeta.get_nodes(board):
                board.place(node)
                n_value = self.alpha_beta(board, depth-1, alpha,beta,False)
                board.undo(node)
                value = max(value,n_value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = self.max_value
            for node in AlphaBeta.get_nodes(board):
                board.place(node)
                n_value = self.alpha_beta(board, depth-1, alpha, beta, True)
                board.undo(node)
                value = min(value,n_value)
                beta = min(beta,value)
                if alpha >= beta:
                    break
            return value

    def make_move(self,board):
        best = -self.max_value
        best_moves = []
        self.nodes_searched = 0
        t_s = time.process_time()
        for node in board.get_available_moves():
            board.place(node)
            self.nodes_searched += 1;
            value = self.alpha_beta(board,self.depth, -self.max_value, self.max_value, False)
            self.nodes_searched += 1;
            board.undo(node)
            if value == best:
                best_moves.append(node)
            elif value > best:
                best = value
                best_moves = [node]
        #print("time:",time.process_time() - t_s);
        best_move = self.random.choice(best_moves)
        board.place(best_move)

#export = AlphaBeta
