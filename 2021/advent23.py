class Board:
    def __init__(self, input=None):
        self.abcd = [(0, 0) for _ in range(8)]
        self.board = []
        self.columns = set()
        if not input:
            return

        for y, row in enumerate(input):
            r = []
            for x, c in enumerate(row):
                if c in 'ABCD':
                    i = (ord(c) - ord('A')) * 2
                    if self.abcd[i] != (0, 0):
                        i += 1
                    self.abcd[i] = y, x
                    self.columns.add(x)
                    c = '.'
                r.append(c)
            self.board.append(r)

    def pos_map(self):
        return {v: chr(ord('A') + i//2) for i, v in enumerate(self.abcd)}

    def __str__(self):
        m = self.pos_map()
        return "\n".join("".join(m.get((y, x), e) for x, e in enumerate(row)) for y, row in enumerate(self.board))

    def __repr__(self):
        return str(self)


def f1(input):
    print()
    b = Board(input)
    print(b)
