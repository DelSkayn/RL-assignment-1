from .player import Player
import numpy as np
import time

TIME_LIMIT = 8

N_PLAYOUTS = 5
CI = 1

LARGE_VALUE = 1_000_000
SMALL_VALUE = -LARGE_VALUE


class Node:
    def __init__(self,move,board,parent):
        self.visits = 1
        self.reward = 0
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

    def best_child(self,ci):
        child_score = [
            x.score(ci) for x in self.children
        ]
        return self.children[np.argmax(child_score)]

    def score(self,ci):
        exploit = self.reward / self.visits;
        expand = ci * np.sqrt( np.log( self.parent.visits) / self.visits)
        return exploit + expand


class MCTS(Player):
    def __init__(self, board_size, color, seed, time_limit = TIME_LIMIT,playouts = N_PLAYOUTS, ci = CI):
        self.ci = ci
        super().__init__(board_size, color, seed)
        self.time_limit = time_limit
        self.playouts = playouts
        self.root = None

    def name():
        return "MCTS"

    def iterate(self):
        # selection and expansion
        node = self.root;
        while not node.is_terminal():
            if not node.is_fully_expanded():
                node = node.expand()
                break;
            else:
                node = node.best_child(self.ci)

        # simulation
        reward_ours = 0
        reward_theres = 0
        if node.board.is_game_over():
            reward_ours = self.playouts
        else:
            for i in range(self.playouts):
                board = node.board.copy()
                while not board.is_game_over():
                    move = board.get_random_move(self.random)
                    board.place(move)
                if board.current_player() != node.board.current_player():
                    reward_ours += 1
                else:
                    reward_theres += 1
        reward_ours /= self.playouts;
        reward_theres /= self.playouts;

        #backpropagation
        while node is not None:
            node.visits += 1
            node.reward += reward_ours
            node.reward -= reward_theres
            node = node.parent
            if node is not None:
                node.visits +=1
                node.reward += reward_theres
                node.reward -= reward_ours
                node = node.parent

    def print_move_list(self):
        order = np.argsort([c.visits for c in self.root.children])
        for o in order:
            n = self.root.children[o]
            n.board.print()
            print("MOVE:", n.move)
            print("SCORE:", n.score(self.ci))
            print("VISITS:", n.visits)

    def recover(self,board):
        if self.root is None:
            self.root = Node((-1,-1),board.copy(),None)
            return;
        new_root = None
        for c in self.root.children:
            if c.board.eq(board):
                new_root = c;
                break
        if new_root is None:
            self.root = Node((-1,-1),board.copy(), None)
        else:
            self.root = new_root
            self.root.parent = None


    def make_move(self,board):
        self.recover(board)
        t_end = time.process_time() + self.time_limit
        i = 0;
        while time.process_time() < t_end:
            self.iterate()
            i+=1
        print("ITERATIONS:",i)
        node_idx = np.argmax([c.visits for c in self.root.children])
        node = self.root.children[node_idx]
        print("SCORE:",node.score(self.ci))
        self.print_move_list()
        self.root = node
        self.root.parent = None
        board.place(node.move)

export = MCTS
