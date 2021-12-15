from util import HV_VARIANTS

""""
x0   N  x10
y0
W         E

y10  S
"""

DIRS = "ESWN"
DIRM = dict(zip(DIRS, HV_VARIANTS))


def parse_line(line):
    return line[0], int(line[1:])


def f1(input):
    direction = "E"
    pos = (0, 0)
    for d, nr in input:
        if d == 'F':
            d = direction
        if d in DIRS:
            dx, dy = DIRM[d]
            pos = (pos[0] + dx * nr, pos[1] + dy * nr)
        elif d in "LR":
            assert nr % 90 == 0
            if d == "L":  # make it a right rotation
                nr = 360 - nr
            dirpos = DIRS.index(direction)
            direction = DIRS[(dirpos + nr // 90) % 4]
    return sum(map(abs, pos))


def f2(input):
    pos = (0, 0)
    way_point = (10, -1)
    for d, nr in input:
        if d == 'F':
            pos = (pos[0] + way_point[0] * nr, pos[1] + way_point[1] * nr)
        elif d in DIRS:
            dx, dy = DIRM[d]
            way_point = (way_point[0] + dx * nr, way_point[1] + dy * nr)
        elif d in "LR":
            if d == "L":  # make it a right rotation
                nr = 360 - nr
            for _ in range(nr // 90):  # rotate right
                way_point = -way_point[1], way_point[0]
    return sum(map(abs, pos))

