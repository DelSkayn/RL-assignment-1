from .mcts import MCTS,Node
import numpy as np
import time

TIME_LIMIT = 8

N_PLAYOUTS = 10

LARGE_VALUE = 1_000_000
SMALL_VALUE = -LARGE_VALUE

class MCTSNoRecover(MCTS):
    def make_move(self,board):
        t_end = time.process_time() + self.time_limit
        self.root = Node((-1,-1), board.copy(),None)
        self.root.visited = 1
        self.recover(board)
        i = 0
        while t_end > time.process_time():
            #print(i)
            i+= 1
            self.iterate()
        best_node = self.get_best_node()
        board.place(best_node.move)
        assert(board.hash() == best_node.board.hash())
        self.root = best_node;
        self.root.parent = None

export = MCTSNoRecover
