import re
from math import sqrt, ceil, floor


def parse_line(line):
    return re.match(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", line).groups()


def f1(input):
    x1, x2, y1, y2 = map(int, input[0])
    max_y = abs(min(y1, y2))

    return (max_y * (max_y-1)) / 2


def f2(input):
    x1, x2, y1, y2 = map(int, input[0])

    min_x = ceil(sqrt(1 + 4 * 2 * x1) - 1)
    max_x = x2
    min_y = y1
    max_y = abs(min(y1, y2))

    for dx in range(min_x, max_x+1):
        for dy in range(min_y, max_y + 1):
            x, y = dx, dy
            while x <= x2 and y >= y1:
                pass # TODO simulate

    print(min_x, max_x, max_y)

    return (min_y * (min_y-1)) / 2
