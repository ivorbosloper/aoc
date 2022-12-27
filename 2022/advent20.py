from io import StringIO
from llist import dllist  # see https://ajakubek.github.io/python-llist/index.html

parse_line = int


def do_mix(nrs):
    length = len(nrs)

    for x in range(length):
        for y in range(length):
            if nrs[y][0] == x:
                number = nrs[y]
                nrs.pop(y)
                if number[1] == -y:
                    nrs.append(number)
                else:
                    nrs.insert((y + number[1]) % (length-1), number)
                break
    return nrs

def f1(nrs):
    nrs = list(enumerate(nrs))
    do_mix(nrs)

    base = next(i for i, v in enumerate(nrs) if v[1] == 0)
    results = [nrs[(base + i) % len(nrs)][1] for i in (1000, 2000, 3000)]
    return sum(results)


def f1(nrs):
    nrs = list((i, v * 811589153) for i, v in enumerate(nrs))
    for t in range(10):
        do_mix(nrs)

    base = next(i for i, v in enumerate(nrs) if v[1] == 0)
    results = [nrs[(base + i) % len(nrs)][1] for i in (1000, 2000, 3000)]
    return sum(results)
