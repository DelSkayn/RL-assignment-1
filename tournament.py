import glob
import numpy as np
import importlib
from hex_skeleton import HexBoard
#from player import Player
from trueskill import Rating, rate_1vs1
import matplotlib
import matplotlib.pyplot as plt


class Tournament:
    def __init__(self,board_size,seed):
        self.size = board_size;
        self.board = None
        self.players = [];

        print("loading players:")
        player_mods = glob.glob("players/*.py")
        for mod in player_mods:
            mod = mod.replace("/",".")[:-3]
            module = importlib.import_module(mod)
            if hasattr(module,'export'):
                print('\t' + mod)
                self.players.append(module.export)


        self.rounds = 0
        self.match_scores = np.zeros((len(self.players), len(self.players)))

        self.b_scores = []
        self.r_scores = []
        self.mixed_scores = []
        for i in range(0, len(self.players)):
            self.b_scores.append(Rating())
            self.r_scores.append(Rating())
            self.mixed_scores.append(Rating())


        self.seed = seed

    def play_round(self):
        self.seed += 1

        for i in range(0,len(self.players)):
            for j in range(0,len(self.players)):
                blue = self.players[i](self.size,HexBoard.BLUE,self.seed)
                red = self.players[j](self.size,HexBoard.RED,self.seed)
                board = HexBoard(self.size)

                blue_turn = True;
                while not board.is_game_over():
                    if blue_turn:
                        blue.make_move(board)
                    else:
                        red.make_move(board)
                    blue_turn = not blue_turn

                if blue_turn:
                    # RED won because it made the wining moves
                    rate_1vs1(self.r_scores[j],self.b_scores[i])
                    if i != j:
                        # Dont rate if playing against once self.
                        rate_1vs1(self.mixed_scores[j], self.mixed_scores[i])
                    self.match_scores[i][j] -= 1
                else:
                    rate_1vs1(self.b_scores[i],self.r_scores[j])
                    if i != j:
                        # Dont rate if playing against once self.
                        rate_1vs1(self.mixed_scores[i], self.mixed_scores[j])
                    self.match_scores[i][j] += 1

    def print_scores(self):
        for i in range(len(self.players)):
            for j in range(len(self.players)):
                print(str(self.match_scores[i][j]) + " ",end='')
            print()

    def show_scores(self):
        names = list(map(lambda x: x.name(x), self.players))
        fig, ax = plt.subplots()
        im = ax.imshow(self.match_scores)
        ax.set_xticks(np.arange(len(names)))
        ax.set_yticks(np.arange(len(names)))
        ax.set_xticklabels(names)
        ax.set_yticklabels(names)
        ax.xaxis.tick_top()
        plt.setp(ax.get_xticklabels(), rotation=-45, ha="right", rotation_mode="anchor")

        for i in range(len(names)):
            for j in range(len(names)):
                text = ax.text(j,i, self.match_scores[i,j], ha="center", va="center", color="w")


        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    print("+++ START +++")
    import argparse
    parser = argparse.ArgumentParser(description="Hex tournament player")
    parser.add_argument("BOARD_SIZE",type = int)
    parser.add_argument("SEED",type = int,nargs='?', default = 0)
    parser.add_argument("NUM_ROUNDS",type = int,nargs='?', default = 20)
    args = parser.parse_args()
    tournament = Tournament(args.BOARD_SIZE, args.SEED)
    for i in range(args.NUM_ROUNDS):
        print("ROUND: " + str(i + 1))
        tournament.play_round()
    tournament.show_scores()
