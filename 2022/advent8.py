from io import StringIO

def parse(input):
    return [[int(x) for x in line.strip()] for line in StringIO(input)]

def f1(maze):
    width, height = len(maze[0]), len(maze)
    visible = [[False for x in row] for row in maze]
    # scan horizontal
    for direction in (range(width), range(width-1, -1, -1)):
        for y, row in enumerate(maze):
            low = -1
            for x in direction:
                h = row[x]
                if h > low:
                    low = h
                    visible[y][x] = True
    # scan vertical
    for direction in (range(height), range(height-1, -1, -1)):
        for x in range(width):
            low = -1
            for y in direction:
                h = maze[y][x]
                if h > low:
                    low = h
                    visible[y][x] = True

    print(sum(v for row in visible for v in row))

def f2(maze):
    width, height = len(maze[0]), len(maze)
    def visible4(y, x):
        # scan horizontal
        h = maze[y][x]
        result = 1
        for direction in (range(x+1, width), range(x-1, -1, -1)):
            t = 0
            for xx in direction:
                t += 1
                if maze[y][xx] >= h:
                    break
            result *= t
        # scan vertical
        for direction in (range(y+1, height), range(y-1, -1, -1)):
            t = 0
            for yy in direction:
                t += 1
                if maze[yy][x] >= h:
                    break
            result *= t
        return result

    print(max(visible4(y, x) for x in range(width) for y in range(height)))
