from util import HZD_VARIANTS, BaseBoard


class Board:
    def __init__(self, input):
        self.board = input
        self.height, self.width = len(self.board), len(self.board[0])

    def new(self, y, x, e):
        if e != '.':
            occupied = sum(self.board[y+dy][x+dx] == '#' for dy, dx in HZD_VARIANTS
                           if 0 <= y+dy < self.height and 0 <= x+dx < self.width)
            if e == 'L':
                if occupied == 0:
                    e = '#'
            else:
                assert e == '#'
                if occupied >= 4:
                    e = 'L'
        return e

    def simulate(self):
        old = self.board
        self.board = ["".join(self.new(y, x, e) for x, e in enumerate(row)) for y, row in enumerate(self.board)]
        return any(old[y] != row for y, row in enumerate(self.board))

    def count(self):
        return sum(e == '#' for row in self.board for e in row)

    def __str__(self):
        return "\n".join(self.board)


def f1(input):
    board = Board(input)
    while board.simulate():
        # print(board, "HOOI")
        pass
    return board.count()


