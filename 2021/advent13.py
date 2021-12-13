import re


class Board:
    def __init__(self, input):
        coords = [(int(line.split(',')[0]), int(line.split(',')[1])) for line in input]
        width, height = max(p[0] for p in coords) + 1, max(p[1] for p in coords) + 1
        self.board = [[False for x in range(width)] for y in range(height)]
        for x, y in coords:
            self.board[y][x] = True

    def __str__(self):
        return "\n".join(["".join(["#" if e else '.' for e in row]) for row in self.board])

    def __repr__(self):
        return str(self)

    def fold_horizontal(self, row):
        new_board = [[e for e in r] for y, r in enumerate(self.board) if y < row]
        for y in range(row + 1, len(self.board)):
            line = self.board[y]
            over_row = row - (y-row)
            if over_row >= 0:
                for x, e in enumerate(line):
                    new_board[over_row][x] |= e
            else:
                new_board.insert(0, line)
        self.board = new_board

    def fold_vertical(self, col):
        width = len(self.board[0])
        new_board = [[e for x, e in enumerate(r) if x < col] for r in self.board]
        for x in range(col + 1, width):
            over_col = col - (x-col)
            if over_col >= 0:
                for y, row in enumerate(self.board):
                    new_board[y][2*col - x] |= row[x]
            else:
                for y, row in enumerate(self.board):
                    new_board[y].insert(0, row[x])
        self.board = new_board

    def count(self):
        return sum(e for row in self.board for e in row)


def f1(input):
    empty_line = input.index('')
    board = Board(input[:empty_line])
    # print()
    # print(board)
    # print()

    for line in input[empty_line+1:]:
        direction, rowcol = re.search("fold along (x|y)=(\d+)", line).groups()
        rowcol = int(rowcol)
        board.fold_horizontal(rowcol) if direction == 'y' else board.fold_vertical(rowcol)
        return board.count()


def f2(input):
    empty_line = input.index('')
    board = Board(input[:empty_line])

    for line in input[empty_line+1:]:
        direction, rowcol = re.search("fold along (x|y)=(\d+)", line).groups()
        rowcol = int(rowcol)
        board.fold_horizontal(rowcol) if direction == 'y' else board.fold_vertical(rowcol)

    print()
    print(board)

