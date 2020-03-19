from .player import Player


# places random neighoring stones
class RandNeighbor(Player):
    def name(self):
        return "Random Neighbor"

    def make_move(self, board):
        neighors = set()
        for i in range(self.size):
            for j in range(self.size):
                if board.is_color((i,j),self.color):
                    for n in board.get_neighbors((i,j)):
                        if board.is_empty(n):
                            neighors.add(n)
        move = None
        if len(neighors) == 0:
            move = board.get_random_move(self.random)
        elif len(neighors) == 1:
            move = neighors.pop()
        else:
            num = self.random.randrange(1,len(neighors))
            for i in range(num):
                move = neighors.pop()
        board.place(move)

#export = RandNeighbor
