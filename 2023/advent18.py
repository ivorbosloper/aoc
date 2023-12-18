import re

from shapely import Polygon

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
MAP = dict(zip("RDLU", DIRS))


def parse_line(line):
    assert (m := re.match(r"([RDLU]) (\d+) \(#(\w+)\)", line))
    d, nr, color = m.groups()
    return d, int(nr), color


def calc(instructions: list[tuple[str, int]]):
    points = []
    x, y = 0, 0
    for d, nr in instructions:
        x += MAP[d][0] * nr
        y += MAP[d][1] * nr
        points.append((y, x))
    return int(Polygon(points).buffer(0.5, cap_style="square", join_style="mitre").area)


def f1(input):
    instructions = [(d, nr) for d, nr, color in input]
    return calc(instructions)


def f2(input):
    instructions = [("RDLU"[int(c[-1])], int(c[:-1], 16)) for d, nr, c in input]
    return calc(instructions)
