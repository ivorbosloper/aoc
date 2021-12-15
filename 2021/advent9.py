from util import HV_VARIANTS


def find_highest_points(input):
    w, h = len(input[0]), len(input)

    def test_higher(ty, tx):
        if 0 <= ty < h and 0 <= tx < w:
            return e < input[ty][tx]
        return True

    highest = []
    for y in range(h):
        for x in range(w):
            e = input[y][x]
            if all(test_higher(y+dy, x+dx) for dx, dy in HV_VARIANTS):
                highest.append((y, x))
    return highest


def f1(input):
    return sum(int(input[y][x]) for y, x in find_highest_points(input))


def f2(input):
    w, h = len(input[0]), len(input)
    highest = find_highest_points(input)
    sizes = []
    handled = [[False for _ in line] for line in input]
    for p in highest:
        size = 0
        queue = [p]
        while len(queue):
            y, x = queue.pop()
            if handled[y][x]:
                continue
            size += 1
            handled[y][x] = True
            for dy, dx in HV_VARIANTS:
                ty, tx = y+dy, x+dx
                if 0 <= ty < h and 0 <= tx < w \
                        and not handled[ty][tx] and "9" > input[ty][tx] > input[y][x]:
                    queue.append((ty, tx))
        sizes.append(size)
    sizes.sort(reverse=True)
    return sizes[0] * sizes[1] * sizes[2]
