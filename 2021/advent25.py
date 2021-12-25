from util import BaseBoard


class Board(BaseBoard):
    def next(self):
        hor = [['>' if c == '.' and row[i-1] == '>' else
                '.' if c == '>' and row[(i+1) % self.width] == '.' else c
                for i, c in enumerate(row)] for row in self.board]
        ver = [['v' if c == '.' and hor[col-1][i] == 'v' else
                '.' if c == 'v' and hor[(col+1) % self.height][i] == '.' else c
                for i, c in enumerate(row)] for col, row in enumerate(hor)]
        return Board(ver, func=lambda x:x)


def f1(input):
    board = Board(input, lambda x: x)
    steps = 0
    while True:
        steps += 1
        new = board.next()
        if board == new:
            return steps
        board = new
