from util import BaseBoard


class Board(BaseBoard):
    def __init__(self, input) -> None:
        super().__init__(input)
        self.board = input
        assert all(c in ("#.") for line in self.board for c in line)
        self.vboard = [
            "".join(input[y][x] for y in range(self.height)) for x in range(self.width)
        ]


def parse(input):
    return [Board(s.split("\n")) for s in input.split("\n\n")]


def calc(board):
    mx = my = 0
    for m in range(1, board.height):
        if all(
            board.board[m - i - 1] == board.board[m + i]
            for i in range(min(m, board.height - m))
        ):
            my = m
            break

    for m in range(1, board.width):
        if all(
            board.vboard[m - i - 1] == board.vboard[m + i]
            for i in range(min(m, board.width - m))
        ):
            mx = m
            break
    assert mx * my == 0
    return 100 * my + mx


def f1(boards):
    # 20297 is too low
    return sum(calc(board) for board in boards)
