class BingoBoard:
    def __init__(self, table=None):
        self.table = table or [[None] * 5 for i in range(5)]
        self.marked = [[False] * 5 for i in range(5)]

    def is_solved(self):
        for i in range(5):
            if all(self.marked[i][j] for j in range(5)) or \
               all(self.marked[j][i] for j in range(5)):
                return True
        return False
        # return all(self.marked[i][i] for i in range(5)) or \
        #        all(self.marked[i][5 - i - 1] for i in range(5))

    def mark(self, nr):
        for y in range(5):
            for x in range(5):
                if self.table[y][x] == nr:
                    self.marked[y][x] = True

    def marked_nrs(self, marked=True):
        return [self.table[y][x] for y in range(5) for x in range(5) if self.marked[y][x] == marked]

    def row_as_str(self, row):
        return " ".join(f"{self.table[row][i]:3}{'*' if self.marked[row][i] else ' '}" for i in range(5))

    def __str__(self):
        return "\n".join(self.row_as_str(row) for row in range(5))

    def __repr__(self):
        return str(self)


def read_boards(input):
    nrs = [int(i) for i in input[0].split(',')]
    boards = []
    table = []
    for line in input[2:]:
        if line:
            table.append([int(i.strip()) for i in line.split(' ') if i])
        else:
            assert len(table) == 5
            boards.append(BingoBoard(table))
            table = []
    if len(table) == 5:
        boards.append(BingoBoard(table))
        table = []
    assert len(table) == 0, table
    return nrs, boards


def f1(input):
    nrs, boards = read_boards(input)
    for nr in nrs:
        for board in boards:
            board.mark(nr)
            if board.is_solved():
                return sum(board.marked_nrs(False)) * nr


def f2(input):
    nrs, boards = read_boards(input)
    solved = set()
    for nr in nrs:
        for board in boards:
            if board in solved:
                continue
            board.mark(nr)
            if not board.is_solved():
                continue
            if len(solved) == len(boards) - 1:
                return sum(board.marked_nrs(False)) * nr
            solved.add(board)
