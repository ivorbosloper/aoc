import re
from collections import defaultdict


def parse_line(line):
    return tuple(int(f) for f in re.split(r'\s+', line))


def f1(input):
    l1 = sorted(a[0] for a in input)
    l2 = sorted(a[1] for a in input)
    return sum(abs(e1-e2) for e1, e2 in zip(l1, l2))


def f2(input):
    histogram = defaultdict(int)
    for e in input:
        histogram[e[1]] += 1

    return sum(a[0] * histogram[a[0]] for a in input)
