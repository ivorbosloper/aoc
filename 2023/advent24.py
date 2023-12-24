from itertools import combinations

from skspatial.objects import Line

Vector = tuple[int, int, int]
DVector = tuple[Vector, Vector]


def mkline(line, max_dims=3) -> Line:
    "19, 13, 30 @ -2,  1, -2"
    return Line(
        *[
            tuple([float(f) for f in e.split(", ")[:max_dims]])
            for e in line.split(" @ ")
        ]
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


def f1(input):
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
