import math
from itertools import combinations

from skspatial.objects import Line

Vector = tuple[int, int, int]
DVector = tuple[Vector, Vector]


def mkline(line, max_dims=3, func=float) -> Line:
    "19, 13, 30 @ -2,  1, -2"
    return Line(
        *[tuple([func(f) for f in e.split(", ")[:max_dims]]) for e in line.split(" @ ")]
    )


def collides(i1: DVector, i2: DVector, dims=3):
    t = None
    for d in range(dims):
        s1, d1, s2, d2 = i1[0][d], i1[1][d], i2[0][d], i2[1][d]
        if d1 == d2:
            if s1 != s2:
                # print(f"parallel, {i1} - {i2}")
                return
        else:
            nt = (s2 - s1) / (d1 - d2)
            if t not in (None, nt):
                return
            t = nt
    assert t is not None
    if t > 0:
        return tuple([i1[0][d] + i1[1][d] * t for d in range(dims)])


def f1_debug(input):
    result = 0

    def debug(*args):
        pass

    # debug = print

    lines = [mkline(line, 2) for line in input]
    box = [7, 27] if len(input) < 10 else [200000000000000, 400000000000000]
    for a, b in combinations(lines, 2):
        debug(f"Hailstone A: {a}")
        debug(f"Hailstone B: {b}")
        try:
            overlap = a.intersect_line(b)
            ta = (overlap[0] - a.point[0]) / a.vector[0]
            tb = (overlap[0] - b.point[0]) / b.vector[0]
            if ta < 0 or tb < 0:
                if tb > 0:
                    text = "hailstone A"
                elif ta > 0:
                    text = "hailstone A"
                else:
                    text = "both hailstones"

                debug(f"paths crossed in the past for {text}")
                debug()
                continue
            if box[0] <= overlap[0] <= box[1] and box[0] <= overlap[1] <= box[1]:
                text = "inside"
                result += 1
            else:
                text = "outside"
            debug(f"Hailstones' paths will cross {text} the test area {overlap}")
        except ValueError as e:
            debug(e)
        debug()
    # 6909 is too low
    return result


def f1_disabled(input):
    result = 0

    lines = [mkline(line, 2) for line in input]
    box = [7, 27] if len(input) < 10 else [200000000000000, 400000000000000]
    for a, b in combinations(lines, 2):
        try:
            overlap = a.intersect_line(b)
            if (overlap[0] - a.point[0]) / a.vector[0] < 0:
                continue
            if (overlap[0] - b.point[0]) / b.vector[0] < 0:
                continue
            if box[0] <= overlap[0] <= box[1] and box[0] <= overlap[1] <= box[1]:
                result += 1
        except ValueError as e:
            pass
    return result


def shared_divisors(nrs: list[int], top=0):
    mx = max(nrs)
    for i in range(1, top or mx // 2 + 1):
        if all(n % i == 0 for n in nrs):
            yield i
    if all(n == mx for n in nrs):
        yield mx


def f2(input):
    # We collide at integer positions. Some of the lines are parallel (seen in f1).
    # Even more of the axis are parallel (x, y or z)
    # A stone can only intersect parallel-axis snow flakes with a speed
    # divisible by the distance between these parallel-axis stuff
    if len(input) < 10:
        return

    test_range = range(400)  # expanded by searching for solutions
    lines = [mkline(line, func=int) for line in input]
    speeds: list[set[int]] = [set() for _ in range(3)]
    for a, b in combinations(lines, 2):
        for d in range(3):
            if a.direction[d] == b.direction[d]:
                diff = b.point[d] - a.point[d]
                lspeeds = set(
                    v
                    for v in test_range
                    if v == a.direction[d] or diff % (v - a.direction[d]) == 0
                )
                speeds[d] = lspeeds if len(speeds[d]) == 0 else speeds[d] & lspeeds

    print(speeds)
    assert all(ds is not None and len(ds) == 1 for ds in speeds)

    s = [next(iter(_)) for _ in speeds]

    # now it's a matter of filling out the formula in any of 2 lines perpendicular
    a, b = lines[4:6]
    da = (a.direction[1] - s[1]) / (a.direction[0] - s[0])
    db = (b.direction[1] - s[1]) / (b.direction[0] - s[0])

    x = ((b.point[1] - (db * b.point[0])) - a.point[1] + (da * a.point[0])) // (da - db)
    y = da * x + (a.point[1] - (da * a.point[0]))
    t = (x - a.point[0]) // (a.direction[0] - s[0])

    z = a.point[2] + (a.direction[2] - s[2]) * t
    return int(x + y + z)

    # divs = [list(shared_divisors(list(ds), top=1000)) for ds in distances]
    # print(divs)
    # for d in range(3):
    #     assert all(a % first_div[d] == 0 for a in distances[d])
