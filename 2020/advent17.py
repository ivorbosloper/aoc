from collections import Counter
from itertools import chain


def surroundings3(x, y, z):
    return ((x + dx, y + dy, z + dz) for dx in range(-1, 2) for dy in range(-1, 2) for dz in range(-1, 2)
            if not dx == dy == dz == 0)


def f1(input):
    field = {(x, y, 0) for y, line in enumerate(input) for x, c in enumerate(line) if c == '#'}
    for _ in range(6):
        counted = Counter(chain.from_iterable(surroundings3(*t) for t in field))
        field = {t for t, cnt in counted.items() if ((t not in field) + 2) <= cnt <= 3}
    return len(field)


def surroundings4(x, y, z, w):
    return ((x + dx, y + dy, z + dz, w+dw)
            for dx in range(-1, 2) for dy in range(-1, 2) for dz in range(-1, 2) for dw in range(-1, 2)
            if not dx == dy == dz == dw == 0)


def f2(input):
    field = {(x, y, 0, 0) for y, line in enumerate(input) for x, c in enumerate(line) if c == '#'}
    for _ in range(6):
        counted = Counter(chain.from_iterable(surroundings4(*t) for t in field))
        field = {t for t, cnt in counted.items() if ((t not in field) + 2) <= cnt <= 3}
    return len(field)
