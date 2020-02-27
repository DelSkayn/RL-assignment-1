from .player import Player

class RandAllNeighbor(Player):
    def name():
        return "Random All Neighbor"

    def make_move(self, board):
        neighors = set()
        for i in range(self.size):
            for j in range(self.size):
                if not board.is_empty((i,j)):
                    for n in board.get_neighbors((i,j)):
                        if board.is_empty(n):
                            neighors.add(n)
        move = None
        if len(neighors) == 0:
            move = self.get_random_move(board)
        elif len(neighors) == 1:
            move = neighors.pop()
        else:
            num = self.random.randrange(1,len(neighors))
            for i in range(num):
                move = neighors.pop()
        board.place(move,self.color)

#export = RandAllNeighbor
