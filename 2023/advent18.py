import re

from shapely import Polygon

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
MAP = dict(zip("RDLU", DIRS))
Pos = tuple[int, int]


def parse_line(line):
    assert (m := re.match(r"([RDLU]) (\d+) \(#(\w+)\)", line))
    d, nr, color = m.groups()
    return d, int(nr), color


class PolygonBuilder:
    def __init__(self, input):
        self.input = input

    def instructions(self):
        return [(d, nr) for d, nr, color in self.input]

    def construct(self):
        points: list[Pos] = []
        x, y = 0, 0
        for d, nr in self.instructions():
            x += MAP[d][0] * nr
            y += MAP[d][1] * nr
            points.append((y, x))
        return Polygon(points).buffer(0.5, cap_style="square", join_style="mitre")


def f1(input):
    return int(PolygonBuilder(input).construct().area)


class PolygonBuilder2(PolygonBuilder):
    def instructions(self):
        return [
            ("RDLU"[int(color[-1])], int(color[:-1], 16)) for d, nr, color in self.input
        ]


def f2(input):
    return int(PolygonBuilder2(input).construct().area)
