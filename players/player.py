import random

# Does random moves
class Player:
    def __init__(self, board_size, color, seed):
        self.size = board_size
        self.color = color
        self.random = random.Random(seed)

    # Makes a random move on the board
    # TODO might be faster to first make a list of possible moves and then select one.
    def get_random_move(self,board):
        coords = (self.random.randrange(0,self.size),self.random.randrange(0,self.size))
        while not board.is_empty(coords):
            coords = (self.random.randrange(0,self.size),self.random.randrange(0,self.size))
        return coords

    def name():
        return "Random"

    # Called when the player needs to make a move
    def make_move(self, board):
        move = self.get_random_move(board)
        board.place(move,self.color)

export = Player
