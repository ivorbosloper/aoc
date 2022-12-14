from io import StringIO
from itertools import pairwise
import copy

def rrange(f, t):
    # inclusive range, any order
    return range(f, t+1) if t>f else range(t, f+1)

class Board:
    def __init__(self, paths) -> None:
        min_x = min(x for path in paths for x, y in path)
        max_x = max(x for path in paths for x, y in path)
        max_y = max(y for path in paths for x, y in path)

        self.shift = min_x
        self.width = max_x - min_x + 1
        self.height = max_y + 1
        self.board = [[' ' for x in range(self.width)] for y in range(self.height)]
        for path in paths:
            for start, end in pairwise(path):
                if start[0] == end[0]:
                    x = start[0]
                    for y in rrange(start[1], end[1]):
                        self.board[y][x - self.shift] = '#'
                else:
                    y = start[1]
                    for x in rrange(start[0], end[0]):
                        self.board[y][x - self.shift] = '#'

    def drop(self):
        x, y = (500-self.shift, 0)
        while True:
            assert self.board[y][x] == ' '
            nx, ny = x, y+1
            # print(nx, ny)
            if ny>=self.height:
                return  # fall through down, gone
            elif self.board[ny][nx] == ' ':
                pass  # go down one
            elif x == 0:
                return # fall trough left, gone
            elif self.board[ny][x-1] == ' ':
                nx = x - 1
            elif x + 1 == self.width:
                return # fall through right, gone
            elif self.board[ny][x+1] == ' ':
                nx = x + 1
            else:
                self.board[y][x] = 'o'
                return 1
            x, y = nx, ny

    def drop2(self):
        x, y = (500-self.shift, 0)
        if self.board[y][x] != ' ':
            return
        while True:
            assert self.board[y][x] == ' '
            nx, ny = x, y+1
            if ny>=self.height:
                self.board[y][x] = 'o'  # bottom
                return 1
            elif self.board[ny][nx] == ' ':
                pass  # go down one
            elif x == 0:
                # expand 10 to left and retry
                self.board = [[' '] * 10 + row for row in self.board]
                self.shift -= 10
                self.width += 10
                x += 10
                continue
            elif self.board[ny][x-1] == ' ':
                nx = x - 1
            elif x + 1 == self.width:
                # expand 10 to right and retry
                self.board = [row + [' '] * 10 for row in self.board]
                self.width += 10
                continue
            elif self.board[ny][x+1] == ' ':
                nx = x + 1
            else:
                self.board[y][x] = 'o'
                return 1
            x, y = nx, ny

    def __str__(self):
        return "\n".join("".join(e for e in row) for row in self.board)


def parse(input):
    paths = [
        [(int(pairs.split(',')[0]), int(pairs.split(',')[1])) for pairs in line.split(' -> ')] 
        for line in StringIO(input)
    ]
    return Board(paths)


def f1(board):
    board = copy.deepcopy(board)
    print(f"Board {board.width} x {board.height}")
    # print(board)
    counter = 0
    while board.drop():
        counter += 1
    print(counter)

def f2(board):
    board = copy.deepcopy(board)
    board.board += [[' ' for x in range(board.width)]]
    board.height += 1

    print()
    print(f"Board {board.width} x {board.height}")
    counter = 0
    while board.drop2():
        counter += 1
    print(counter)
