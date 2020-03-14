import argparse
import importlib
from hexboard import HexBoard

parser = argparse.ArgumentParser(description="Hex interactive player")
parser.add_argument("BOARD_SIZE",type = int)
parser.add_argument("PLAYER_RED",help="The red player",type = str,nargs='?', default = "player")
parser.add_argument("PLAYER_BLUE",help="The blue player",type = str,nargs='?', default = "player")
parser.add_argument("SEED",type = int,nargs='?', default = None)
args = parser.parse_args()

try:
    c_blue = importlib.import_module("players." + args.PLAYER_BLUE).export
    c_red = importlib.import_module("players." + args.PLAYER_RED).export
    p_blue = c_blue(args.BOARD_SIZE,HexBoard.BLUE,args.SEED)
    p_red = c_red(args.BOARD_SIZE,HexBoard.RED,args.SEED)
except ModuleNotFoundError:
    print("Invalid player name")
    exit(-1)

print(c_blue.name() + " VS " + c_red.name())
board = HexBoard(args.BOARD_SIZE)
is_blue_turn = True
while not board.is_game_over():
    if is_blue_turn:
        assert(board.current_player() == HexBoard.BLUE)
        print("BLUE turn:")
        board.print()
        p_blue.make_move(board)
    else:
        assert(board.current_player() == HexBoard.RED)
        print("RED turn:")
        board.print()
        p_red.make_move(board)
    is_blue_turn = not is_blue_turn
    board.print()

if is_blue_turn:
    print("RED " + c_red.name() + " won!")
else:
    print("BLUE " + c_blue.name() + " won!")
