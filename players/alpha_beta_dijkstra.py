from .alpha_beta import AlphaBeta
from hex_skeleton import HexBoard
from heapq import heapify, heappop, heappush

class AlphaBetaDijkstra(AlphaBeta):

    def __init__(self, board_size, color, seed):
        super().__init__(board_size, color, seed)
        self.depth = 3

    def name():
        return "Alpha Beta Dijkstra"

    def shortest_path(self,start,color,board,shorter_then):
        if board.is_empty(start):
            p_que = [(1,start)]
        elif board.is_color(start,color):
            p_que = [(0,start)]
        else:
            return;
        done = set({start})
        heapify(p_que)
        while len(p_que) > 0:
            l,node = heappop(p_que)
            # Reached the edge
            if node[0] == self.size -1 and color == HexBoard.BLUE:
                return l
            if node[1] == self.size -1 and color == HexBoard.RED:
                return l
            # If we reached a longer path we can stop trying to find a short path
            if l == shorter_then:
                return None
            for n in board.get_neighbors(node):
                # If empty increase the length because we need to make a move
                if board.is_empty(n):
                    if n not in done:
                        done.add(n)
                        heappush(p_que,(l+1,n))
                # If there is already a node of our color we dont need to move
                # So we dont need to increase the length
                if board.is_color(n,color):
                    if n not in done:
                        done.add(n)
                        heappush(p_que,(l,n))


    def eval(self, board, maxi):
        if board.is_game_over():
            if maxi:
                return -self.max_value
            else:
                return self.max_value
        # Just to make sure that lenght will always be larger then the path
        our_length = self.size * self.size
        for i in range(self.size):
            if self.color == HexBoard.BLUE:
                start = (0,i)
            else:
                start = (i,0)
            new_length = self.shortest_path(start,self.color,board,our_length)
            if new_length is not None:
                our_length = min(our_length,new_length)

        if not maxi:
            our_length += 1

        there_length = self.size * self.size
        for i in range(self.size):
            if self.other_color == HexBoard.BLUE:
                start = (0,i)
            else:
                start = (i,0)
            new_length = self.shortest_path(start,self.other_color,board,there_length)
            if new_length is not None:
                there_length = min(there_length,new_length)

        return there_length - our_length


export = AlphaBetaDijkstra
