import re


def parse_line(line):
    return tuple(map(int, re.split(",| -> ", line)))


class Board:
    def __init__(self, x_size, y_size):
        self.board = [[0 for i in range(x_size)] for y in range(y_size)]

    def draw_horizontal_vertical(self, t):
        if t[0] == t[2]:
            y1, y2 = (t[1], t[3]) if t[3] > t[1] else (t[3], t[1])
            for y in range(y1, y2+1):
                self.board[y][t[0]] += 1
            return True
        elif t[1] == t[3]:
            x1, x2 = (t[0], t[2]) if t[2] > t[0] else (t[2], t[0])
            for x in range(x1, x2+1):
                self.board[t[1]][x] += 1
            return True
        return False

    def draw_diagonal(self, t):
        if abs(t[0] - t[2]) == abs(t[1] - t[3]):
            x_range = range(t[0], t[2]+1) if t[0] - t[2] < 0 else range(t[0], t[2]-1, -1)
            y_range = range(t[1], t[3]+1) if t[1] - t[3] < 0 else range(t[1], t[3]-1, -1)
            for x, y in zip(x_range, y_range):
                self.board[y][x] += 1
            return True
        return False

    def sum(self, func):
        return sum(func(cell) for row in self.board for cell in row)

    def __str__(self):
        return "\n".join(" ".join([str(cell) if cell else '.' for cell in row]) for row in self.board)

    def __repr__(self):
        return str(self)


def make_board(input):
    x_size = max(max(t[0] for t in input), max(t[2] for t in input)) + 1
    y_size = max(max(t[1] for t in input), max(t[3] for t in input)) + 1
    return Board(x_size, y_size)


def f1(input):
    board = make_board(input)
    for coords in input:
        board.draw_horizontal_vertical(coords)
    return board.sum(lambda cell: cell >= 2)


def f2(input):
    board = make_board(input)
    for coords in input:
        assert board.draw_horizontal_vertical(coords) or board.draw_diagonal(coords)
    return board.sum(lambda cell: cell >= 2)
