from .mcts import MCTS,Node
import numpy as np
import time

TIME_LIMIT = 8

N_PLAYOUTS = 10

LARGE_VALUE = 1_000_000
SMALL_VALUE = -LARGE_VALUE

class MCTSNoRecover(MCTS):

    def name(self):
        return "MCTS NO RE " + str(self.playouts) + " " + str(self.ci)

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
        node_idx = np.argmax([c.visits for c in self.root.children])
        best_node = self.root.children[node_idx]
        board.place(best_node.move)
        self.root = best_node;
        self.root.parent = None

export = MCTSNoRecover
