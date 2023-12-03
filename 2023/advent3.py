import re
from collections import defaultdict


def is_symbol(s: str):
    return (not s.isdigit()) and s != "."


class Board:
    def __init__(self, input):
        self.board = input
        self.height = len(self.board)
        self.width = len(self.board[0])

    def get_nrs(self):
        for y, row in enumerate(self.board):
            if m := re.finditer(r"\d+", row):
                for mg in m:
                    yield mg.start(), y, mg.group(0)

    def check(self, x, y, base=None):
        return is_symbol(self.get(x, y))

    def next_to_symbol(self, x, y, s):
        base = (x, y, s)
        lx = len(s)
        if any(
            self.check(x - 1, y + i, base) or self.check(x + lx, y + i, base)
            for i in range(-1, 2)
        ):
            return True

        return any(
            self.check(i, y - 1, base) or self.check(i, y + 1, base)
            for i in range(x, x + lx)
        )

    def get(self, x, y, default="."):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.board[y][x]
        return default


def f1(input):
    board = Board(input)
    return sum(int(s) for x, y, s in board.get_nrs() if board.next_to_symbol(x, y, s))


class Board2(Board):
    def __init__(self, input):
        super().__init__(input)
        self.gears = defaultdict(list)  # (x, y) --> [(x, y, len)]

    def check(self, x, y, base):
        if self.get(x, y) == "*":
            self.gears[(x, y)].append(base)
            return True


def f2(input):
    board = Board2(input)
    for x, y, s in board.get_nrs():
        board.next_to_symbol(x, y, s)
    return sum(
        int(bases[0][2]) * int(bases[1][2])
        for bases in board.gears.values()
        if len(bases) == 2
    )
