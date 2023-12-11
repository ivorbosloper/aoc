from util import BaseBoard


class Board(BaseBoard):
    def __init__(self, input, multiple=2):
        super().__init__(input)
        self.multiple = multiple
        self.xs = set(
            x
            for x in range(self.width)
            if all(self.board[y][x] == "." for y in range(self.height))
        )
        self.ys = set(
            y
            for y in range(self.height)
            if all(self.board[y][x] == "." for x in range(self.width))
        )
        self.locations = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.board[y][x] == "#"
        ]

    def distance(self, p1, p2):
        x1, x2 = (p1[0], p2[0]) if p1[0] < p2[0] else (p2[0], p1[0])
        y1, y2 = (p1[1], p2[1]) if p1[1] < p2[1] else (p2[1], p1[1])
        base_dist = x2 - x1 + y2 - y1
        factor = self.multiple - 1

        return (
            base_dist
            + sum(factor for y in range(y1, y2) if y in self.ys)
            + sum(factor for x in range(x1, x2) if x in self.xs)
        )

    def all_distances(self):
        return sum(
            self.distance(p1, p2)
            for index, p1 in enumerate(self.locations)
            for p2 in self.locations[index + 1 :]
        )


def f1(input):
    return Board(input).all_distances()


def f2(input):
    return Board(input, multiple=1000000).all_distances()
