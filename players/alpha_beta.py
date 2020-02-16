from .player import Player
from hex_skeleton import HexBoard
import math

class AlphaBeta(Player):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.depth = 3
        self.other_color = HexBoard.RED
        self.killer_moves = []
        for i in range(self.depth + 1):
            self.killer_moves.append(None)
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
            k_move = self.killer_moves[depth]
            if k_move is not None and board.is_empty(k_move):
                board.place(k_move,self.color)
                value = max(value, self.alpha_beta(board,depth-1,alpha,beta,False))
                board.undo_place(k_move)
                alpha = max(alpha,value)
                #if alpha >= beta:
                    #return value

            for node in AlphaBeta.get_nodes(board):
                if node == k_move:
                    continue
                board.place(node,self.color)
                n_value = self.alpha_beta(board, depth-1, alpha,beta,False)
                board.undo_place(node)
                if n_value > value:
                    value = n_value
                    self.killer_moves[depth] = node

                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            k_move = self.killer_moves[depth]
            if k_move is not None and board.is_empty(k_move):
                board.place(k_move,self.other_color)
                value = min(value, self.alpha_beta(board,depth-1,alpha,beta,True))
                board.undo_place(k_move)
                beta = min(beta,value)
                #if alpha >= beta:
                    #return value

            for node in AlphaBeta.get_nodes(board):
                if k_move is not None and node == k_move:
                    continue
                board.place(node,self.other_color)
                n_value = self.alpha_beta(board, depth-1, alpha, beta, True)
                board.undo_place(node)
                if n_value < value:
                    value = n_value
                    self.killer_moves[depth] = node
                beta = min(beta,value)
                if alpha >= beta:
                    break
            return value

    def make_move(self,board):
        for i in range(self.depth + 1):
            self.killer_moves[i] = None
        best = -math.inf
        best_move = self.get_random_move(board)
        self.nodes_searched = 0
        for node in AlphaBeta.get_nodes(board):
            board.place(node,self.color)
            self.nodes_searched += 1;
            value = self.alpha_beta(board,self.depth, -math.inf, math.inf, False)
            self.nodes_searched += 1;
            board.undo_place(node)
            if value > best:
                best = value
                best_move = node
        board.place(best_move,self.color)

export = AlphaBeta
