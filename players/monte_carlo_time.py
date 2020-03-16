from .player import Player
import time
import numpy as np

# A simple monte carlo player which plays 10 random games
# for each possible move and then picks the one which
# wins the most amount of times
class MonteCarloTime(Player):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.time_limit = 8

    def name():
        return "MonteCarlo Time"

    def play_random_game(self,board):
        while not board.is_game_over():
            move = board.get_random_move(self.random)
            board.place(move)
        if board.current_player() == self.color:
            return 1
        return 0



    def make_move(self,board):
        t_end = time.process_time() + self.time_limit
        moves = board.get_available_moves()
        score = np.zeros(len(moves));
        while t_end > time.process_time():
            new_scores = np.zeros(len(moves))
            for i,m in enumerate(moves):
                board.place(m)
                new_scores[i] += self.play_random_game(board.copy())
                board.undo(m)
            score += new_scores
        move = moves[np.argmax(score)]
        board.place(move)

export = MonteCarloTime
