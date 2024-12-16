from typing import Generic, TypeVar

HV_VARIANTS = ((1, 0), (0, 1), (-1, 0), (0, -1))
HZD_VARIANTS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))


T = TypeVar("T")


class BaseBoard(Generic[T]):
    func = lambda x: x

    def __init__(self, input, func=None):
        func = func or self.__class__.func
        self.board: list[list[T]] = [[func(i) for i in row] for row in input]
        self.height = len(self.board)
        self.width = len(self.board[0])

    def __str__(self):
        return "\n".join("".join(str(e) for e in row) for row in self.board)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.board == other.board

    def __ne__(self, other):
        return not self.__eq__(other)

    def get(self, x: int, y: int, default=None) -> T | None:
        return (
            self.board[y][x]
            if 0 <= x < self.width and 0 <= y < self.height
            else default
        )

    def find(self, e: T, default=None) -> tuple[int, int]:
        for y, row in enumerate(self.board):
            for x, c in enumerate(row):
                if c == e:
                    return x, y
