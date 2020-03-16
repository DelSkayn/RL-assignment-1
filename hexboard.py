import numpy as np
import copy

class HexBoard:
    EMPTY = 0
    BLUE = 1
    RED = 2

    def __init__(self,size):
        self.board = np.zeros((size,size),dtype=np.int8)
        self.size = size
        self.game_over = False
        self.cur_player_blue = True

    def copy(self):
        return copy.deepcopy(self)

    def hash(self):
        val = 0
        for i in range(self.size):
            for j in range(self.size):
                val += self.board[i,j]
                val *= 4
        return val

    def eq(self,other):
        return np.all(self.board == other.board)

    def is_game_over(self):
        return self.game_over

    def is_empty(self,coords):
        x,y = coords
        return self.board[x,y] == HexBoard.EMPTY

    def is_color(self,coords,color):
        x,y = coords
        return self.board[x,y] == color

    def get(self,coords):
        x,y = coords
        return self.board[x,y]

    def get_available_moves(self):
        return np.argwhere(self.board == HexBoard.EMPTY)

    def current_player(self):
        if self.cur_player_blue:
            return HexBoard.BLUE
        else:
            return HexBoard.RED

    def place(self,coords):
        x,y = coords
        if not self.game_over and self.is_empty(coords):
            self.board[x,y] = self.current_player()
            if self.check_win(coords):
                self.game_over = True
            else:
                self.cur_player_blue = not self.cur_player_blue
        else:
            self.print()
            print("MOVE:",coords)
            if not self.is_empty(coords):
                raise Exception("INVALID BOARD: move position is not empty")
            if self.game_over:
                raise Exception("INVALID BOARD: game already over")

    def undo(self,coords):
        x,y = coords
        if not self.game_over:
            self.cur_player_blue = not self.cur_player_blue
        self.game_over = False
        self.board[x,y] = HexBoard.EMPTY

    def get_random_move(self,random):
        moves = np.argwhere(self.board == HexBoard.EMPTY)
        return random.choice(moves)

    def get_neighbors(self,coords):
        x,y = coords
        if x-1 >= 0:
            yield (x-1,y)
        if x+1 < self.size:
            yield (x+1,y)
        if x-1 >= 0 and y+1 < self.size:
            yield (x-1,y+1)
        if x+1 < self.size and y-1 >= 0:
            yield (x+1,y-1)
        if y+1 < self.size:
            yield (x,y+1)
        if y-1>=0:
            yield (x,y-1)

    def check_win(self,move):
        x,y = move
        left = False
        right = False
        visited = {}
        visited[(x,y)] = True
        pending = [(x,y)]
        color = self.current_player()
        if color == HexBoard.BLUE:
            left |= x == 0
            right |= x == self.size - 1
        else:
            left |= y == 0
            right |= y == self.size - 1
        while len (pending) > 0:
            move = pending.pop()
            for n in self.get_neighbors(move):
                x,y = n
                if not self.is_color(n, color) or (n in visited): continue
                if color == HexBoard.BLUE:
                    left |= x == 0
                    right |= x == self.size - 1
                else:
                    left |= y == 0
                    right |= y == self.size - 1
                if left and right:
                    return True
                visited[n] = True
                pending.append(n)
        return False


    def print(self):
        print("   ",end="")
        for y in range(self.size):
            print(chr(y+ord('a')),"",end="")
        print("")
        print(" -----------------------")
        for y in range(self.size):
            print(y, "|",end="")
            for z in range(y):
                print(" ", end="")
            for x in range(self.size):
                piece = self.board[x,y]
                if piece == HexBoard.BLUE: print("b ",end="")
                elif piece == HexBoard.RED: print("r ",end="")
                else:
                    if x==self.size:
                        print("-",end="")
                    else:
                        print("- ",end="")
            print("|")
        print("   -----------------------")
        if self.cur_player_blue:
            print("TURN: BLUE");
        else:
            print("TURN: RED");
