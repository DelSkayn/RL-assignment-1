from .alpha_beta_dijkstra import AlphaBetaDijkstra

#Increases the depth of alpha beta dijkstra

class AlphaBetaDijkstra4(AlphaBetaDijkstra):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.depth = 4


#export = AlphaBetaDijkstra4
