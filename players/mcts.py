from .player import Player
import numpy as np
import time

TIME_LIMIT = 1

N_PLAYOUTS = 10

LARGE_VALUE = 1_000_000
SMALL_VALUE = -LARGE_VALUE


class Node:
    def __init__(self,move,board,parent):
        self.visited = 0
        self.score = 0
        self.parent = parent;
        self.move = move
        self.board = board
        self.children = []
        self.untried_moves = list(self.board.get_available_moves());

    def is_terminal(self):
        return self.board.is_game_over()

    def is_leaf(self):
        return len(self.children) == 0

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def expand(self):
        move = self.untried_moves.pop()
        new_board = self.board.copy()
        new_board.place(move)
        node = Node(move,new_board,self)
        self.children.append(node)
        return node

    def best_child(self):
        child_score = [
            x.UCB() for x in self.children
        ]
        return self.children[np.argmax(child_score)]


    def UCB(self):
        if self.visited == 0:
            return LARGE_VALUE
        return self.score + 2 * np.sqrt(np.log(self.parent.visited) / self.visited)


class MCTS(Player):
    def __init__(self, board_size, color, seed, time_limit = TIME_LIMIT,playouts = N_PLAYOUTS):
        super().__init__(board_size, color, seed)
        self.time_limit = time_limit
        self.playouts = playouts

    def name():
        return "Monte Carlo tree search"

    def playout(self,board):
        score = 0
        for i in range(self.playouts):
            c_board = board.copy()
            while not c_board.is_game_over():
                move = c_board.get_random_move(self.random)
                c_board.place(move)
            if c_board.current_player() == self.color:
                score += 1
            else:
                score -= 1
        return score

    def select(self):
        cur = self.root
        while not cur.is_terminal():
            if not cur.is_fully_expanded():
                return cur.expand()
            else:
                cur = cur.best_child()
        return cur

    def backpropagate(self,node,score):
        while node is not None:
            node.score += score
            node.visited += 1
            node = node.parent


    def iterate(self):
        node = self.select()
        score = self.playout(node.board)
        self.backpropagate(node,score)

    def get_move(self):
        return self.root.best_child().move

    def make_move(self,board):
        t_end = time.process_time() + self.time_limit
        self.root = Node((-1,-1),board,None)
        # Avoid doing playouts for the root node.
        self.root.visited = 1;
        i = 0
        while t_end > time.process_time():
            #print(i)
            i+= 1
            self.iterate()
        board.place(self.get_move())

export = MCTS
