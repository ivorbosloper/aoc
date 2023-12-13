from util import BaseBoard


class Board(BaseBoard):
    def __init__(self, input) -> None:
        super().__init__(input)
        # self.board = input
        assert all(c in ("#.") for line in self.board for c in line)
        self.vboard = [
            [input[y][x] for y in range(self.height)] for x in range(self.width)
        ]


def parse(input):
    return [Board(s.split("\n")) for s in input.split("\n\n")]


def calc(board, skip=None):
    mx = my = 0
    for m in range(1, board.height):
        if skip and skip[0] == m:
            continue
        if all(
            board.board[m - i - 1] == board.board[m + i]
            for i in range(min(m, board.height - m))
        ):
            my = m
            break

    for m in range(1, board.width):
        if skip and skip[1] == m:
            continue
        if all(
            board.vboard[m - i - 1] == board.vboard[m + i]
            for i in range(min(m, board.width - m))
        ):
            mx = m
            break
    assert mx * my == 0
    return 100 * my + mx


def f1(boards):
    return sum(calc(board) for board in boards)


def calc2(board):
    current = calc(board)
    skip = current // 100, current % 100
    result = 0
    b = board.board
    for y in range(board.height):
        for x in range(board.width):
            b[y][x] = "#" if b[y][x] == "." else "."
            m = calc(board, skip)
            b[y][x] = "#" if b[y][x] == "." else "."
            if m != 0:
                assert result in (0, m)
                result = m
    return result


def f2(boards):
    # 32192 correct
    return sum(calc2(board) for board in boards)
