import sys

from util import HZD_VARIANTS


def f1(input):
    visited = set()
    dir: int = 0
    location: tuple = (0, 0)
    visited.add(location)
    # HZD_VARIANTS[dir]
    for line in input:
        command, arg = line.split(" ")
        arg = int(arg)
        if command == "draai":
            dir = (dir + arg // 45) % 8
        elif command in ("loop", "spring"):
            v = HZD_VARIANTS[dir]
            for i in range(1, arg + 1):
                visited.add((location[0] + v[0] * i, location[1] + v[1] * i))
            location = location[0] + v[0] * arg, location[1] + v[1] * arg
        else:
            raise ValueError(f"Command unknown: {command}")

    box = [0, 0, 0, 0]  # x1, y1, x2, y2
    for v in visited:
        if v[0] < box[0]:
            box[0] = v[0]
        elif v[0] > box[2]:
            box[2] = v[0]
        if v[1] < box[1]:
            box[1] = v[1]
        elif v[1] > box[3]:
            box[3] = v[1]

    print()
    for y in range(box[2], box[0], -1):
        for x in range(box[1], box[3] + 1):
            sys.stdout.write("#" if (y, x) in visited else " ")
        print()

    # Pakjesavond
    return sum(location)
