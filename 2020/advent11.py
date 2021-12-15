from util import HZD_VARIANTS, BaseBoard


class Board:
    def __init__(self, input):
        self.board = input
        self.height, self.width = len(self.board), len(self.board[0])
        self.tolerance = 4
        self.adjecents = None

    def adj1(self, y, x):
        return [(y + dy, x + dx) for dy, dx in HZD_VARIANTS
                if 0 <= y + dy < self.height and 0 <= x + dx < self.width and
                self.board[y + dy][x + dx] == 'L']

    def fill_1(self):
        self.adjecents = [[self.adj1(y, x) for x in range(self.width)] for y in range(self.height)]

    def adj2(self, y, x):
        result = []
        if self.board[y][x] == 'L':
            for dy, dx in HZD_VARIANTS:
                ny, nx = y + dy, x + dx
                found = False
                while not found and 0 <= ny < self.height and 0 <= nx < self.width:
                    if self.board[ny][nx] == 'L':
                        result.append((ny, nx))
                        found = True
                    ny, nx = ny + dy, nx + dx
        return result

    def fill_2(self):
        self.adjecents = [[self.adj2(y, x) for x in range(self.width)] for y in range(self.height)]
        self.tolerance = 5

    def new(self, y, x, e):
        if e != '.':
            occupied = sum(self.board[y][x] == '#' for y, x in self.adjecents[y][x])
            if e == 'L':
                if occupied == 0:
                    e = '#'
            else:
                assert e == '#'
                if occupied >= self.tolerance:
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
    board.fill_1()
    while board.simulate():
        pass
    return board.count()


def f2(input):
    board = Board(input)
    board.fill_2()
    while board.simulate():
        pass
    return board.count()

