from copy import deepcopy

from util import BaseBoard, HV_VARIANTS
DIRS = ">v<^"


def parse(inp):
    iboard, moves = inp.split("\n\n")
    return Board(iboard.split("\n")), moves.replace("\n", "")


class Board(BaseBoard[str]):
    def __init__(self, input, func=None):
        super().__init__(input)
        for y, line in enumerate(input):
            if '@' in line:
                x = line.index('@')
                self.pos = (x, y)
                self.board[y][x] = "."

    def __str__(self):
        x, y = self.pos
        return "\n".join("".join("@" if i == x and j == y else e
                         for i, e in enumerate(row)) for j, row in enumerate(self.board))

    def score(self, target="O"):
        result = 0
        for y, line in enumerate(self.board):
            for x, c in enumerate(line):
                if c == target:
                    result += y * 100 + x
        return result

    def move(self, m):
        dx, dy = HV_VARIANTS[DIRS.index(m)]
        new_x, new_y = self.pos[0] + dx, self.pos[1] + dy
        if self.board[new_y][new_x] == ".":
            self.pos = (new_x, new_y)
        elif self.board[new_y][new_x] == "#":
            pass
        else:
            assert self.board[new_y][new_x] == "O"
            nx, ny = new_x, new_y
            while self.board[ny][nx] == "O":
                nx, ny = nx + dx, ny + dy
            if self.board[ny][nx] == ".":
                self.pos = (new_x, new_y)
                self.board[new_y][new_x] = "."
                self.board[ny][nx] = "O"

    def move2(self, m):
        dx, dy = HV_VARIANTS[DIRS.index(m)]
        new_x, new_y = self.pos[0] + dx, self.pos[1] + dy
        if self.board[new_y][new_x] == ".":
            self.pos = (new_x, new_y)
        elif self.board[new_y][new_x] == "#":
            pass
        else:
            if dx:
                nx = new_x
                while self.board[new_y][nx] in "[]":
                    nx += dx
                if self.board[new_y][nx] == ".":  # can move
                    # breakpoint()
                    for i, x in enumerate(range(new_x+dx, nx+dx, dx)):
                        self.board[new_y][x] = "[]"[(i + (dx == -1)) % 2]
                    self.pos = (new_x, new_y)
                    self.board[new_y][new_x] = "."
                return

            replacements = [(new_x - "[]".index(self.board[new_y][new_x]), new_y)]
            total_replacements = list(replacements)
            while replacements:
                new_replacements = set()
                for r in replacements:
                    nx, ny = r[0] + dx, r[1] + dy
                    space = self.board[ny][nx] + self.board[ny][nx+1]
                    if "#" in space:
                        return  # total failure, can not move at all
                    if space[0] in '[]':
                        new_replacements.add((nx - "[]".index(space[0]), ny))
                    if space[1] == '[':
                        new_replacements.add((nx + 1, ny))
                replacements = list(new_replacements)
                total_replacements.extend(replacements)

            for r in reversed(total_replacements):
                ox, oy = r[0], r[1]
                nx, ny = r[0] + dx, r[1] + dy
                assert self.board[ny][nx] == "." and self.board[ny][nx+1] == '.'
                assert self.board[oy][ox] == "[" and self.board[oy][ox+1] == ']'
                self.board[ny][nx] = "["; self.board[ny][nx + 1] = ']'
                self.board[oy][ox] = "."; self.board[oy][ox + 1] = '.'

            self.pos = new_x, new_y

    def explode(self):
        mapping = {"#": "##", "O": "[]", ".": "..", "@": "@."}
        self.board = [[e for c in row for e in mapping[c]] for row in self.board]
        self.pos = (self.pos[0] * 2, self.pos[1])
        self.width *= 2


def f1(inp):
    board, moves = inp
    board = deepcopy(board)
    # print(board)
    # print()
    for m in moves:
        # print("Move", m)
        board.move(m)
        # print(board)
        # print()

    return board.score()


def f2(inp):
    board, moves = inp
    board.explode()
    for i, m in enumerate(moves):
        board.move2(m)
        # print(board)
        # print()
    return board.score("[")
