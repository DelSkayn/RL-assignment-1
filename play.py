import argparse
import importlib
from hexboard import HexBoard

parser = argparse.ArgumentParser(description="Hex interactive player")
parser.add_argument("BOARD_SIZE",type = int)
parser.add_argument("-r",help="play as red",action="store_true")
parser.add_argument("PLAYER",type = str,nargs='?', default = "player")
parser.add_argument("SEED",type = int,nargs='?', default = 0)
args = parser.parse_args()

opp_color = HexBoard.RED
play_color = HexBoard.BLUE
if args.r:
    opp_color = HexBoard.BLUE
    play_color = HexBoard.RED

board = HexBoard(args.BOARD_SIZE)
board.print()
opponent_class = importlib.import_module("players." + args.PLAYER).export
opponent = opponent_class(args.BOARD_SIZE,opp_color,args.SEED)


print("Playing vs: " + opponent_class.name())

is_player_turn = not args.r
while not board.is_game_over():
    if is_player_turn:
        try:
            text_in = input("move?> ")
            x,y = text_in.split(',')
            x = int(x)
            y = ord(y) - ord('a')
            if x >= 0 and x < board.size and y >= 0 and y < board.size and board.is_empty((y,x)):
                board.place((y,x))
                is_player_turn = not is_player_turn
            else:
                print("invalid move")
        except ValueError:
            print("invalid move")
    else:
        print("opponent move:")
        opponent.make_move(board)
        is_player_turn = not is_player_turn
    board.print()

if is_player_turn:
    print("you lost..")
else:
    print("you won!!")
