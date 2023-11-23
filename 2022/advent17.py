SHAPES = (
    tuple((i, 0) for i in range(4)),
    ((1,0), (0,1), (1,1), (2,1), (1, 2)),
    ((2,0), (2,1), (0,2), (1,2), (2, 2)),
    tuple((0, i) for i in range(4)),
    ((0,0), (1,0), (0,1), (1,1)),
)
DIM_SHAPES = tuple(
    (max(xy[0] for xy in shape) + 1, max(xy[1] for xy in shape) + 1) for shape in SHAPES
)

parse = str.strip

def f1(input):
    board = Board(input)
    for _ in range(2022):
        board.step()
    return board.height()

def f2(input):
    # start with initial state (i_pointer, s_pointer)
    # simulated, stop whenever a line is 'full'
    # cache((i_pointer, s_pointer) is current height)
    # empty-line == empty slate
    # cache space is 10.000 i_pointers x 5 shapes

    # Then, detect the cycle. Divide the huge number by the cycle, and simulate the rest
    board = Board(input)
    cache = {}  # (s_pointer, i_pointer, start_state) --> (height, steps, shape_pointer, shift_pointer, board)
    steps = 0
    while True:
        key = (board.s_pointer, board.i_pointer, str(board))
        if key in cache:
            # we found a cycle
            break
        local_steps = 0
        while not board.tetris_2lines():
            board.step()
            local_steps += 1
        height = board.height()
        steps += local_steps
        board.renew(keep_from=board.tetris_2lines())
        cache[key] = (height-board.height(), local_steps, board.s_pointer, board.i_pointer, str(board))
    
    # steps until now are valid
    # cut the simulations by using the cycle as far as possible.
    # then, simulate the last steps manually

    height, steps, sp, ip, brd = cache[key]
    assert (sp, ip, brd) in cache
    print(height, steps, sp, ip, brd)



class Board:
    def __init__(self, input):
        self.input = input
        self.s_pointer = 0
        self.i_pointer = 0
        self.top_line = 0
        self.space = None
        self.renew()
    
    def height(self):
        return self.top_line

    def tetris(self):
        for row in range(self.top_line-3, self.top_line+1):
            if row > 0 and all(c != ' ' for c in self.space[row]):
                return row

    def tetris_2lines(self):
        for row in range(self.top_line-3, self.top_line):
            if row>0 and all(self.space[row][i] != ' ' or self.space[row][i+1] != ' ' for i in range(1, 8)):
                return row

    def renew(self, keep_from=None):
        keep = self.space[keep_from:] if keep_from else []
        self.space = [['='] * 9] + keep + [['|'] + [' ']*7 + ['|'] for i in range(5000)]
        self.top_line = self.top_line-keep_from-1 if keep_from else 0

    def shift(self):
        shift = self.input[self.i_pointer]
        self.i_pointer = (self.i_pointer + 1) % len(self.input)
        return -1 if shift == '<' else 1

    def step(self):
        shape = SHAPES[self.s_pointer]
        dims = DIM_SHAPES[self.s_pointer]
        self.s_pointer = (self.s_pointer + 1) % 5

        x = 3  # left offset
        y = self.top_line + 3 + dims[1]  # top offset

        while True:
            if y + 10 > len(self.space):
                self.space += [['|'] + [' ']*7 + ['|'] for i in range(5000)]
            new_x, new_y = x + self.shift(), y - 1
            if all(self.space[y - sy][new_x + sx] == ' ' for sx, sy in shape):
                x = new_x
            if not all(self.space[new_y - sy][x + sx] == ' ' for sx, sy in shape):
                break
            y = new_y

        for sx, sy in shape:
            self.space[y - sy][x + sx] = '#'
        if y > self.top_line:
            self.top_line = y

    def __str__(self) -> str:
        return "\n".join("".join(self.space[r]) for r in range(self.top_line, -1, -1))

