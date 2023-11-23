import math
from collections import Counter


def scores(input):
    w, h = len(input[0]), len(input)

    def direction(x1, y1, x2, y2):
        if input[y2][x2] != "#" or (x1 == x2 and y1 == y2):
            return
        dx, dy = x2 - x1, y2 - y1
        div = math.gcd(abs(dx), abs(dy))
        return (dx // div, dy // div)  # direction

    def score(sx, sy):
        if input[sy][sx] != "#":
            return None

        # directions = set()
        directions = dict(
            Counter(direction(sx, sy, x, y) for y in range(h) for x in range(w))
        )
        directions.pop(None)
        return (sx, sy), directions

    iterator = (score(x, y) for y in range(h) for x in range(w))
    return (i for i in iterator if i)


def f1(input):
    return max(len(directions) for point, directions in scores(input))


def f2(input):
    point, directions = max(scores(input), key=lambda p: len(p[1]))

    counter = 0
    depth = 0
    while counter < 200:
        steps = sorted(
            (d for d, v in directions.items() if v),
            key=lambda d: math.atan2(d[0], -d[1]),
        )
        depth += 1
        for s in steps:
            counter += 1
            directions[s] -= 1
            if counter == 200:
                break

    print(counter, len(directions), depth, s, point)

    hits = 0
    x, y = point

    while hits < depth:
        x += s[0]
        y += s[1]
        if input[y][x] == "#":
            hits += 1

    # 3412 too high, 1628 too low. 1822 too low
    return y * 100 + x
