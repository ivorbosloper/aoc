HV_VARIANTS = ((1, 0), (0, 1),  (-1, 0), (0, -1))
HZD_VARIANTS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))


class BaseBoard:
    def __init__(self, input, func=int):
        self.board = [[func(i) for i in row] for row in input]
        self.width = len(self.board)
        self.height = len(self.board[0])

    def __str__(self):
        return "\n".join("".join(str(e) for e in row) for row in self.board)

    def __repr__(self):
        return str(self)
