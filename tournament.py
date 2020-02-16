import glob
import numpy as np
import importlib
from hex_skeleton import HexBoard
#from player import Player
from trueskill import Rating, rate_1vs1
from joblib import Parallel, delayed
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

    def run_match(self,blue,red):
        b = self.players[blue](self.size,HexBoard.BLUE,self.seed)
        r = self.players[red](self.size,HexBoard.RED,self.seed)
        board = HexBoard(self.size)

        blue_turn = True;
        while not board.is_game_over():
            if blue_turn:
                b.make_move(board)
            else:
                r.make_move(board)
            blue_turn = not blue_turn

        return not blue_turn, blue,red


    def process_winner(self,blue_won, blue, red):
        if blue_won:
            b,r = rate_1vs1(self.b_scores[blue],self.r_scores[red])
            self.b_scores[blue] = b
            self.r_scores[red] = r
            if blue != red:
                # Dont rate if playing against once self.
                a,b = rate_1vs1(self.mixed_scores[blue], self.mixed_scores[red])
                self.mixed_scores[blue] = a
                self.mixed_scores[red] = b
            self.match_scores[blue][red] += 1
        else:
            # RED won because it made the wining moves
            r,b = rate_1vs1(self.r_scores[red],self.b_scores[blue])
            self.r_scores[red] = r
            self.r_scores[blue] = b
            if blue != red:
                # Dont rate if playing against once self.
                a,b = rate_1vs1(self.mixed_scores[red], self.mixed_scores[blue])
                self.mixed_scores[red] = a
                self.mixed_scores[blue] = b


    def play_round(self):
        self.seed += 1

        l = len(self.players)
        wins = Parallel(n_jobs=-1,verbose=10)(delayed(self.run_match)(i,j) for i in range(l) for j in range(l))
        for blue_won, blue,red in wins:
            self.process_winner(blue_won,blue,red)
        #for i in range(0,len(self.players)):
        #    for j in range(0,len(self.players)):


    def print_scores(self):
        for i in range(len(self.players)):
            for j in range(len(self.players)):
                print(str(self.match_scores[i][j]) + " ",end='')
            print()

    def show_scores(self):
        names = np.array(list(map(lambda x: x.name(), self.players)))
        order = np.argsort(self.mixed_scores)
        names = names[order]
        match_scores = self.match_scores[order]
        for i in range(len(match_scores)):
            match_scores[i] = match_scores[i][order]
        fig, ax = plt.subplots()
        ax.imshow(match_scores)
        ax.set_xticks(np.arange(len(names)))
        ax.set_yticks(np.arange(len(names)))
        ax.set_xticklabels(names)
        ax.set_yticklabels(names)
        ax.xaxis.tick_top()
        plt.setp(ax.get_xticklabels(), rotation=-45, ha="right", rotation_mode="anchor")

        for i in range(len(names)):
            for j in range(len(names)):
                ax.text(j,i, match_scores[i,j], ha="center", va="center", color="w")

        fig.tight_layout()
        plt.show()

    def print_elo(self):
        print("Mixed scores:")
        for i in range(len(self.mixed_scores)):
            print(self.players[i].name() + " " + str(self.mixed_scores[i]))
        print()
        print("Blue scores:")
        for i in range(len(self.b_scores)):
            print(self.players[i].name() + " " + str(self.b_scores[i]))
        print()
        print("Red scores:")
        for i in range(len(self.r_scores)):
            print(self.players[i].name() + " " + str(self.r_scores[i]))
        print()


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
    tournament.print_elo()
    tournament.show_scores()
