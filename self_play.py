import argparse
import importlib
from hex_skeleton import HexBoard

parser = argparse.ArgumentParser(description="Hex interactive player")
parser.add_argument("BOARD_SIZE",type = int)
parser.add_argument("PLAYER_RED",help="The red player",type = str,nargs='?', default = "player")
parser.add_argument("PLAYER_BLUE",help="The blue player",type = str,nargs='?', default = "player")
parser.add_argument("SEED",type = int,nargs='?', default = None)
args = parser.parse_args()

try:
    p_blue = importlib.import_module("players." + args.PLAYER_BLUE).export(args.BOARD_SIZE,HexBoard.BLUE,args.SEED)
    p_red = importlib.import_module("players." + args.PLAYER_RED).export(args.BOARD_SIZE,HexBoard.RED,args.SEED)
except ModuleNotFoundError:
    print("Invalid player name")
    exit(-1)

print(p_blue.name() + " VS " + p_red.name())
board = HexBoard(args.BOARD_SIZE)
is_blue_turn = True
while not board.is_game_over():
    if is_blue_turn:
        print("BLUE turn:")
        p_blue.make_move(board)
    else:
        print("RED turn:")
        p_red.make_move(board)
    is_blue_turn = not is_blue_turn
    board.print()

if is_blue_turn:
    print("RED " + p_red.name() + " won!")
else:
    print("BLUE " + p_blue.name() + " won!")
