from util import BaseBoard

# E, S, W, N
HV_VARIANTS = ((1, 0), (0, 1), (-1, 0), (0, -1))
E, S, W, N = HV_VARIANTS


class Board(BaseBoard):
    def tilt(self, direction=N):
        board = self.board
        for y in range(self.height):
            for x, block in enumerate(board[y]):
                if block in "#O" or self.get(x + direction[0], y + direction[1]) == ".":
                    continue
                assert block == "."
                # now scan down until you find an O (or stop on something else)
                nx, ny = x - direction[0], y - direction[1]
                while self.get(nx, ny) == ".":
                    nx, ny = nx - direction[0], ny - direction[1]
                found = self.get(nx, ny, "#")
                if found == "#":
                    continue
                assert found == "O"
                board[y][x] = "O"
                board[ny][nx] = "."

    def weight(self):
        return sum(
            (self.height - y)
            for x in range(self.width)
            for y in range(self.height)
            if self.board[y][x] == "O"
        )


def f1(input):
    board = Board(input)
    board.tilt(direction=N)
    return board.weight()
