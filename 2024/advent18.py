from util import BaseBoard, HV_VARIANTS
from collections import deque


class Board(BaseBoard):
    def __init__(self, inp):
        super().__init__("\n")
        self.width = self.height = 7 if len(inp) < 1000 else 71
        self.board = [[None for _x in range(self.width)] for _y in range(self.height)]
        for i, line in enumerate(inp.splitlines()):
            x, y = map(int, line.split(","))
            self.board[y][x] = i

    def search(self, comparator):
        q = deque()
        fastest = [[None for _x in range(self.width)] for _y in range(self.height)]
        q.append((0, 0))
        fastest[0][0] = 0
        while q:
            x, y = q.popleft()
            current = fastest[y][x]
            assert current is not None
            for dx, dy in HV_VARIANTS:
                nx, ny = x + dx, y + dy
                block = self.get(nx, ny, 1)
                if block is not None and block < comparator:
                    continue
                # field still accessible
                if fastest[ny][nx] is None:
                    fastest[ny][nx] = current + 1
                    q.append((nx, ny))
        return fastest[self.height-1][self.width-1]

    def index(self, block):
        for y, row in enumerate(self.board):
            for x, c in enumerate(row):
                if c == block:
                    return x, y


def parse(inp):
    return Board(inp)


def f1(board):
    return board.search(12 if board.width == 7 else 1024)


def f2(board):
    for i in range(12 if board.width == 7 else 1024, 10000):
        if board.search(i) is None:
            # print(i, board.index(i-1))
            return ",".join([str(s) for s in board.index(i-1)])
