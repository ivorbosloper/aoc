import re
from functools import reduce
from operator import mul
regex = re.compile(r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)")

f1_dim = 50
f1_max = f1_dim*2


def parse_line(line):
    return tuple(int(g)+f1_dim if i > 0 else g == 'on' for i, g in enumerate(regex.match(line).groups()))


def min_max(c1, c2):
    r = range(max(0, c1), min(f1_max, c2))
    if r:
        return r.start, r.stop


def f1(input):
    world = [[[False for _ in range(f1_max+1)] for __ in range(f1_max+1)] for ___ in range(f1_max+1)]
    for line in input:
        toggle = line[0]
        try:
            x1, x2 = min_max(line[1], line[2])
            y1, y2 = min_max(line[3], line[4])
            z1, z2 = min_max(line[5], line[6])
        except:
            continue
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    world[x][y][z] = toggle

    return sum(e for block in world for line in block for e in line)


class Cube:
    def __init__(self, on, *coords):  # x1, x2, y1, y2, z1, z2
        self.on = on
        self.coords = coords

    def overlap(self, b):
        if not any(b.coords[i] > self.coords[i+1] or self.coords[i] > b.coords[i+1] for i in (0, 2, 4)):
            return Cube(True, *((min if i % 2 else max)([self.coords[i], b.coords[i]]) for i in range(6)))

    def area(self):
        return reduce(mul, ((abs(self.coords[i+1] - self.coords[i]) + 1) for i in (0, 2, 4)), 1)


def f2(input):
    handled = []
    for line in input:
        cube = Cube(*line)
        cut_outs = []  # either positive or negative cut_outs on the handled cubes (and handled cut_outs),
                       # caused by the newly added cube
        # The algorithm is exponential, but way more efficient than working with all the voxels
        for other in handled:
            overlap = other.overlap(cube)
            if overlap is None:
                continue
            if other.on == cube.on:  # subtract
                overlap.on = not cube.on
            else:
                overlap.on = not other.on
            cut_outs.append(overlap)

        if cube.on:
            handled.append(cube)
        handled.extend(cut_outs)

    return sum(cube.area() if cube.on else -cube.area() for cube in handled)
