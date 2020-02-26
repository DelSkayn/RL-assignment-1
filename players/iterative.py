from .alpha_beta_dijkstra import AlphaBetaDijkstra
from hex_skeleton import HexBoard
import math
import sys

class Interative(AlphaBetaDijkstra):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.t_table = {};
        self.move_table = {};
        self.depth = 4


    def name():
        return "Iterative"

    def gen_moves(self,board):
        k_move = self.move_table.get(board.hash())
        if k_move and board.is_empty(k_move):
            #print("hit move")
            yield k_move

        for i in range(board.size):
            for j in range(board.size):
                if board.is_empty((i,j)) and (i,j) != k_move:
                    yield (i,j)

    def alpha_beta(self,board, depth, alpha, beta, maxi):
        self.nodes_searched += 1
        tv = self.t_table.get((board.hash(),depth))
        if tv:
            return tv
        if depth == 0 or board.is_game_over():
            return self.eval(board, maxi)
        elif maxi:
            best = -math.inf
            best_move = None
            for node in self.gen_moves(board):
                board.place(node, self.color)
                value = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.undo_place(node)
                if value > best:
                    best = value
                    best_move = node
                alpha = max(alpha,value)
                if alpha >= beta:
                    break
        else:
            best = math.inf
            best_move = None
            for node in self.gen_moves(board):
                board.place(node, self.other_color)
                value = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.undo_place(node)
                if value < best:
                    best = value
                    best_move = node
                beta = min(beta, value)
                if alpha >= beta:
                    break;
        self.move_table[board.hash()] = best_move
        self.t_table[(board.hash(), depth)] = best
        return best

    def make_move(self,board):
        depth = 0
        total_best_move = None
        for i in range(self.depth):
            self.nodes_searched = 0
            best_move = None
            best = -math.inf
            for node in self.gen_moves(board):
                board.place(node,self.color)
                value = self.alpha_beta(board, depth, best, math.inf, False)
                board.undo_place(node)
                if value > best:
                    best = value
                    best_move = node
            total_best_move = best_move
            self.move_table[board.hash()] = best_move
            depth += 1
        if total_best_move is None:
            total_best_move = self.get_random_move(board)
        board.place(total_best_move, self.color)

export = Interative
