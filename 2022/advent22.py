import re

HV_VARIANTS = ((1, 0), (0, 1),  (-1, 0), (0, -1))

def parse(input):
    maze = input.split('\n')
    instructions = maze.pop()
    maze.pop()
    y_min_max = [[None, -100000] for c in maze[0]]
    x_min_max = []
    for y, row in enumerate(maze):
        mn, mx = None, None
        for x, c in enumerate(row):
            if c != ' ':
                if mn is None:
                    mn = x
                mx = x

                ymm = y_min_max[x]
                if ymm[0] is None:
                    ymm[0] = y
                ymm[1] = y
        x_min_max.append((mn, mx))

    return maze, instructions, x_min_max, y_min_max

def f1(mz):
    maze, instructions, x_min_max, y_min_max = mz

    x, y, direction = x_min_max[0][0], 0, 0
    assert maze[y][x] == '.'
    for instr in re.findall("(\d+|R|L)", instructions):
        # print(f"INSTR: {instr}, dir={HV_VARIANTS[direction]}")
        if instr == 'L':
            direction = (direction + 3) % 4
        elif instr == 'R':
            direction = (direction + 1) % 4
        else:
            steps = int(instr)
            diff = HV_VARIANTS[direction]
            for i in range(steps):
                # nx, ny is new location
                if diff[0]:
                    nx, ny = x + diff[0], y
                    mm = x_min_max[y]
                    if nx < mm[0]:
                        nx = mm[1]
                    elif nx > mm[1]:
                        nx = mm[0]
                else:
                    nx, ny = x, y + diff[1]
                    mm = y_min_max[x]
                    if ny < mm[0]:
                        ny = mm[1]
                    elif ny > mm[1]:
                        ny = mm[0]

                c = maze[ny][nx]
                assert c != ' '
                if c == '.':  # if open, go there
                    print(nx, ny)
                    x, y = nx, ny

    return (1+y)*1000 + 4 *(1+x) + direction
