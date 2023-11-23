import re


def parse_line(line):
    m = re.match("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
    return tuple(map(int, m.groups()))


class Board:
    def __init__(self, input) -> None:
        self.board = [0] * (1000 * 1000)
        self.input = input

    def play(self):
        for claim, px, py, w, h in self.input:
            for y in range(py * 1000, (py + h) * 1000, 1000):
                for x in range(px, px + w):
                    self.board[y + x] += 1

    def find_not_overlapping(self):
        for claim, px, py, w, h in self.input:
            if all(
                self.board[y + x] == 1
                for y in range(py * 1000, (py + h) * 1000, 1000)
                for x in range(px, px + w)
            ):
                return claim


def f1(input):
    board = Board(input)
    board.play()
    return sum(1 for b in board.board if b > 1)


def f2(input):
    board = Board(input)
    board.play()
    return board.find_not_overlapping()
