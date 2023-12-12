cache = {}


def options(line, nrs):
    if not nrs:
        return "#" not in line

    key = tuple([line, *nrs])
    if key not in cache:
        first, *nrs = nrs

        # one extra space between each group is required
        to_fill = sum(g + 1 for g in nrs) - 1
        cache[key] = sum(
            options(line[first + i + 1 :], nrs)
            for i in range(len(line) - to_fill - first)
            if all(c in (ok, "?") for c, ok in zip(line, "." * i + "#" * first + "."))
        )
    return cache[key]


def parse_line(line):
    a, b = line.split(" ")
    return a, tuple(int(i) for i in b.split(","))


def f1(input):
    return sum(options(line, nrs) for line, nrs in input)


def f2(input):
    input = [("?".join([a] * 5), b * 5) for a, b in input]
    return sum(options(line, nrs) for line, nrs in input)
