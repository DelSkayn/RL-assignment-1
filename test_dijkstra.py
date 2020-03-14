from hex_skeleton import HexBoard
from heapq import heapify, heappop, heappush
import copy

def shortest_path(start,board,shorter_then):
    if board.is_empty(start):
        p_que = [(1,start)]
    elif board.is_color(start,HexBoard.BLUE):
        p_que = [(0,start)]
    else:
        return board.size * board.size, [];
    done = set({start})
    paths = {}
    paths[start] = None
    heapify(p_que)
    while len(p_que) > 0:
        l,node = heappop(p_que)
        # Reached the edge
        if node[0] == board.size-1:
            cur = node
            path = []
            while cur is not None:
                path.append(cur)
                cur = paths[cur]
            return l, path
        # If we reached a longer path we can stop trying to find a short path
        if l == shorter_then:
            return board_size * board_size,[]
        for n in board.get_neighbors(node):
            # If empty increase the length because we need to make a move
            if board.is_empty(n):
                if n not in done:
                    done.add(n)
                    paths[n] = node
                    heappush(p_que,(l+1,n))
            # If there is already a node of our color we dont need to move
            # So we dont need to increase the length
            if board.is_color(n,HexBoard.BLUE):
                if n not in done:
                    done.add(n)
                    paths[n] = node
                    heappush(p_que,(l,n))


board_size = int(input("board size?>"))
board = HexBoard(board_size)
while True:
    board.print()
    print("options are: place, path")
    inp = input("input?>")
    if inp == "place":
        color = input("color?>")
        if color == "blue" or color == "":
            play_color = HexBoard.BLUE
        else:
            play_color = HexBoard.RED
        text_in = input("move?> ")
        x,y = text_in.split(',')
        x = int(x)
        y = ord(y) - ord('a')
        if x >= 0 and x < board.size and y >= 0 and y < board.size and board.is_empty((y,x)):
            board.place((y,x),play_color)
        else:
            print("invalid move")
    elif inp == "path":
        our_length = board_size * board_size
        path = None
        for i in range(board_size):
            start = (0,i)
            new_length,p = shortest_path(start,board,our_length)
            if new_length < our_length:
                our_length = new_length
                path = p
        tmp_board = copy.deepcopy(board)
        for p in path:
            print(p)
            if tmp_board.is_empty(p):
                tmp_board.place(p, HexBoard.BLUE)
        tmp_board.print()
    else:
        print("invalid command")
