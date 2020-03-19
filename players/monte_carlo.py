from .player import Player

# A simple monte carlo player which plays 10 random games
# for each possible move and then picks the one which
# wins the most amount of times
class MonteCarlo(Player):

    def __init__(self, board_size, color, seed, num_tries = 10):
        super().__init__(board_size, color, seed)
        self.num_tries = num_tries

    def name(self):
        return "MonteCarlo " + str(self.num_tries)

    def play_random_game(self,board):
        while not board.is_game_over():
            move = board.get_random_move(self.random)
            board.place(move)
        if board.current_player() == self.color:
            return 1
        return 0



    def make_move(self,board):
        best_score = -1
        for i in range(0,self.size):
            for j in range(self.size):
                if board.is_empty((i,j)):
                    score = 0
                    board.place((i,j))
                    for k in range(self.num_tries):
                        # Dont bother if we cant get a better score
                        if self.num_tries - k + score <= best_score:
                            break
                        tmp_board = board.copy()
                        score += self.play_random_game(tmp_board)
                    #print("SCORE:",score);
                    #board.print()
                    board.undo((i,j))
                    if score > best_score:
                        best_score = score
                        best = (i,j)
        board.place(best)

#export = MonteCarlo
