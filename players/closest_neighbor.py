from .player import Player
from hexboard import HexBoard

# A player which tries to create a path by placing
# the neighboring stone which is the closest to the other end of the board
class ClosestNeighbor(Player):
    def name(self):
        return "Closest Neighbor"

    def make_move(self, board):
        best = 0
        move = None
        # Find the neighbour closest to the edge
        for i in range(self.size):
            for j in range(self.size):
                if board.is_color((i,j),self.color):
                    for (x,y) in board.get_neighbors((i,j)):
                        if not board.is_empty((x,y)):
                            continue
                        if self.color == HexBoard.BLUE:
                            if x >= best:
                                move = (x,y)
                                best = x
                        else:
                            if y >= best:
                                move = (x,y)
                                best = y

        # If there are no neighbours make a random move at the edge of the board
        if move is None:
            num = self.random.randrange(1,self.size)
            if self.color == HexBoard.BLUE:
                move = (0,num)
            else:
                move = (num,0)
        # If that move is already present give up and just walk the board from
        # one edge to another till we find an empty spot
        if not board.is_empty(move):
            for i in range(self.size):
                found = False
                for j in range(self.size):
                    if self.color == HexBoard.BLUE:
                        move = (i,j)
                    else:
                        move = (j,i)
                    found = board.is_empty(move)
                    if found:
                        break
                if found:
                    break
        board.place(move)

#export = ClosestNeighbor
