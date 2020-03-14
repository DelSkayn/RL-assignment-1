import random

# Does random moves
class Player:
    def __init__(self, board_size, color, seed):
        self.size = board_size
        self.color = color
        self.random = random.Random(seed)

    def name():
        return "Random"

    # Called when the player needs to make a move
    def make_move(self, board):
        move = board.get_random_move(self.random)
        board.place(move)

export = Player
