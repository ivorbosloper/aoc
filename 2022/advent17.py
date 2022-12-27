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
    s_pointer = 0

    space = [['='] * 9] + [['|'] + [' ']*7 + ['|'] for i in range(10000)]
    top_line = 0

    def shift():
        i_pointer = 0
        while True:
            shift = input[i_pointer]
            i_pointer = (i_pointer + 1) % len(input)
            assert shift in ('<', '>'), shift
            yield -1 if shift == '<' else 1
    shifter = shift()

    for _ in range(2022):
        shape = SHAPES[s_pointer]
        dims = DIM_SHAPES[s_pointer]
        s_pointer = (s_pointer + 1) % 5
        x = 3  # left offset
        y = top_line + 3 + dims[1]  # top offset

        while True:
            new_x, new_y = x + next(shifter), y - 1
            if all(space[y - sy][new_x + sx] == ' ' for sx, sy in shape):
                x = new_x  # it fits
                # print(f"shift to {new_x}")
            # else:
            #     print(f"no shift to {new_x}")
            if not all(space[new_y - sy][x + sx] == ' ' for sx, sy in shape):
                break
            y = new_y

        for sx, sy in shape:
            space[y - sy][x + sx] = '#'
        if y > top_line:
            top_line = y

    print(_)
    for r in range(top_line+1, -1, -1):
        print("".join(space[r]))

    return top_line

def f2(input):
    # start with initial state (i_pointer, s_pointer)
    # simulated, stop whenever a line is 'full'
    # cache((i_pointer, s_pointer) is current height)
    # empty-line == empty slate
    # cache space is 10.000 i_pointers x 5 shapes
    pass
