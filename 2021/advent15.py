import sys
from queue import PriorityQueue
from util import HV_VARIANTS, BaseBoard


def mod9(i):
    return (i-1) % 9 + 1


class Board(BaseBoard):
    def shortest_path(self):
        queue = PriorityQueue()
        cost = [[sys.maxsize for x in range(self.width)] for y in range(self.height)]
        cost[0][0] = 0
        queue.put((0, 0, 0))
        while not queue.empty():
            current_cost, y, x = queue.get()
            if current_cost > cost[y][x]:
                continue
            for dy, dx in HV_VARIANTS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    new_cost = self.board[ny][nx] + current_cost
                    if new_cost < cost[ny][nx]:
                        cost[ny][nx] = new_cost
                        queue.put((new_cost, ny, nx))
        return cost[-1][-1]

    def times_5(self):
        board = Board([[]])
        board.width = self.width * 5
        board.height = self.height * 5
        board.board = [[mod9(self.board[y % self.height][x % self.width] + (y//self.height) + (x//self.width))
                        for x in range(board.width)] for y in range(board.height)]
        return board


def f1(input):
    board = Board(input)
    return board.shortest_path()


def f2(input):
    board = Board(input).times_5()
    return board.shortest_path()
