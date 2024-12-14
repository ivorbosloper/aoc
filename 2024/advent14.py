import re
import math
from collections import defaultdict

regex = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')


def parse(inp):
    return [list(map(int, regex.match(line).groups())) for line in inp.splitlines()]


def f1(inp):
    wx, wy = 101, 103
    if len(inp) < 20:
        wx, wy = 11, 7
    hx, hy = wx//2, wy//2
    times = 100

    q = [0, 0, 0, 0]
    for px, py, vx, vy in inp:
        px, py = (px + vx * times) % wx, (py + vy * times) % wy
        if px == hx or py == hy:
            continue
        i = px // (hx+1) + 2 * (py // (hy+1))
        q[i] += 1

    return math.prod(q)


def f2(inp):
    wx, wy = 101, 103
    block = 8
    if len(inp) < 20:
        wx, wy = 11, 7
        block = 2

    def pprint(s):
        counts = defaultdict(int)
        for p in s:
            counts[p] += 1
        print()
        for y in range(wy):
            print("".join(str(counts.get((x, y), ".")) for x in range(wx)))

    for times in range(1, 10000):
        s = set()
        for px, py, vx, vy in inp:
            s.add(((px + vx * times) % wx, (py + vy * times) % wy))

        # Not very efficient, could jump x if found something
        for y in range(wy - block):
            for x in range(wx - block):
                found = all((x2, y2) in s for x2 in range(x, x+block) for y2 in range(y, y+block))
                if found:
                    pprint(s)
                    print(y, x, times)
                    return times
    assert False
