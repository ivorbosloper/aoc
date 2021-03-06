HV_VARIANTS = ((1, 0), (0, 1),  (-1, 0), (0, -1))
HZD_VARIANTS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))


class BaseBoard:
    def __init__(self, input, func=int):
        self.board = [[func(i) for i in row] for row in input]
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
