from .alpha_beta_dijkstra import AlphaBetaDijkstra
from hex_skeleton import HexBoard
from heapq import heapify, heappop, heappush

#Increases the depth of alpha beta dijkstra

class AlphaBetaDijkstra4(AlphaBeta):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.depth = 4

    def name():
        return "Alpha Beta Dijkstra Depth 4"


export = AlphaBetaDijkstra4
