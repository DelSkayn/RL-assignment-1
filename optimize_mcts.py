import glob
import numpy as np
import importlib
from players.mcts import MCTS
from players.mcts_no_recover import MCTSNoRecover
from hexboard import HexBoard
#from player import Player
from trueskill import Rating, rate_1vs1
from joblib import Parallel, delayed
import matplotlib.pyplot as plt


class Tournament:
    def __init__(self,board_size,seed):
        self.size = board_size;
        self.board = None
        self.players = []
        self.rounds_played = 0

        cis = [0.1,0.2,0.5,1.0,2.0,4.0]
        playouts = [1,2,5,10,20]
        players = [MCTS,MCTSNoRecover]

        all_players = [(p,o,c) for p in players for o in playouts for c in cis]
        self.players = all_players
        print(self.players)
        self.names = [None for i in range(len(self.players))]

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
        b_args = self.players[blue]
        r_args = self.players[red]
        b = b_args[0](self.size,HexBoard.BLUE,self.seed, playouts = b_args[1], ci = b_args[2])
        r = r_args[0](self.size,HexBoard.RED,self.seed, playouts = r_args[1], ci = r_args[2])
        if self.names[blue] is None:
            self.names[blue] = b.name()
        if self.names[red] is None:
            self.names[red] = r.name()
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


    def play_round(self,par):
        self.seed += 1

        l = len(self.players)
        wins = par(delayed(self.run_match)(i,j) for i in range(l) for j in range(l))
        for blue_won, blue,red in wins:
            self.process_winner(blue_won,blue,red)
        self.rounds_played += 1


    def print_scores(self):
        for i in range(len(self.players)):
            for j in range(len(self.players)):
                print(str(self.match_scores[i][j]) + " ",end='')
            print()

    def show_scores(self):
        names = np.array(list(map(lambda x: x.name(), self.players)))
        order = np.argsort(self.mixed_scores)
        names = names[order]
        match_scores = self.match_scores[order] / self.rounds_played
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
    tournament = Tournament(5, 0)
    with Parallel(n_jobs=15,verbose=10,) as par:
        for i in range(20):
            print("ROUND: " + str(i + 1))
            tournament.play_round(par)
    tournament.print_elo()
    tournament.show_scores()
