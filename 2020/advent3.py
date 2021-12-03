def g(slope, raster):
    w, h = len(raster[0]), len(raster)
    x, y = 0, 0

    count = 0
    while True:
        x = (x+slope[0]) % w
        y += slope[1]
        if y >= h:
            break
        count += raster[y][x] == '#'
    return count


def f1(input):
    slope = 3, 1
    return g(slope, input)


def f2(input):
    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    counts = [g(slope, input) for slope in slopes]
    cnt = 1
    for i in counts:
        cnt *= i
    return cnt
