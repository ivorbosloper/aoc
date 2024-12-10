from collections import defaultdict

from util import BaseBoard, HV_VARIANTS


class Board(BaseBoard[int]):
    func = int


def parse(input):
    return Board(input.split("\n"))


def f1(board):
    current = {(x, y): {(x, y)} for y, row in enumerate(board.board) for x, c in enumerate(row) if c == 9}
    for step in range(8, -1, -1):
        new = defaultdict(set)
        for pos, origins in current.items():
            x, y = pos
            for dx, dy in HV_VARIANTS:
                if board.get(x+dx, y+dy) == step:
                    new[(x+dx, y+dy)].update(origins)
        current = new

    assert all(board.board[y][x] == 0 for x, y in current)
    return sum(len(e) for e in current.values())


def f2(board):
    current = {(x, y): 1 for y, row in enumerate(board.board) for x, c in enumerate(row) if c == 9}

    for step in range(8, -1, -1):
        new = defaultdict(int)
        for pos, nr_paths in current.items():
            x, y = pos
            for dx, dy in HV_VARIANTS:
                if board.get(x+dx, y+dy) == step:
                    new[(x+dx, y+dy)] += nr_paths
        current = new

    assert all(board.board[y][x] == 0 for x, y in current)
    return sum(current.values())
