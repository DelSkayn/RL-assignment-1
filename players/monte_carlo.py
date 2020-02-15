from .player import Player
from hex_skeleton import HexBoard
import copy

class MonteCarlo(Player):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.num_tries = 10

    def name(self):
        return "MonteCarlo 10"

    def play_random_game(self,board):
        # Our move has already been done
        # So it is the blue turn if we are not blue
        blue_turn = self.color != HexBoard.BLUE

        while not board.is_game_over():
            move = self.get_random_move(board)
            if blue_turn:
                board.place(move,HexBoard.BLUE)
            else:
                board.place(move,HexBoard.RED)
            blue_turn = not blue_turn

        if blue_turn == self.color != HexBoard.BLUE:
            return 1
        return 0



    def make_move(self,board):
        best = self.get_random_move(board);
        best_score = 0
        for i in range(0,self.size):
            for j in range(self.size):
                if board.is_empty((i,j)):
                    score = 0
                    for k in range(self.num_tries):
                        # Dont bother if we cant get a better score
                        if self.num_tries - k + score <= best_score:
                            break
                        tmp_board = copy.deepcopy(board)
                        tmp_board.place((i,j),self.color)
                        score += self.play_random_game(tmp_board)
                    if score > best_score:
                        best_score = score
                        best = (i,j)
        board.place(best,self.color)

#export = MonteCarlo
