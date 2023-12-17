import operator
import sys


def power(x, y, grid_serial):
    rack_id = x + 10
    return (((rack_id * y + grid_serial) * rack_id) // 100 % 10) - 5


class Board:
    def __init__(self, grid_serial) -> None:
        self.size = 300
        self.board = [
            [power(x, y, grid_serial) for x in range(self.size)]
            for y in range(self.size)
        ]

    def find_sums(self, size=3):
        # use dynamic programming. Keep an array (length-y) of sums(x..., y)
        for y in range(self.size - size):
            for x in range(self.size - size):
                yield x, y, sum(
                    self.board[y + dy][x + dx]
                    for dy in range(size)
                    for dx in range(size)
                )

    def max_sum_rectangle(self):
        mx = my = msum = 0
        for y in range(self.size):
            sys.stdout.write(f"{y}.")
            for x in range(self.size):
                summed = 0
                for s in range(self.size - max(x, y)):
                    summed += sum(self.board[y + s][x : x + s]) + sum(
                        self.board[y + d][x] for d in range(s)
                    )
                    if summed > msum:
                        msum = summed
                        mx, my = x, y
        return mx, my, msum


def f1(input):
    assert power(122, 79, 57) == -5
    assert power(217, 196, 39) == 0
    assert power(101, 153, 71) == 4
    board = Board(int(input[0]))
    return max(board.find_sums(), key=operator.itemgetter(2))


def f2(input):
    board = Board(int(input[0]))
    return board.max_sum_rectangle()
