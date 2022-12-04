import re

def contains(p1, p2):
    return p1[0] <= p2[0] and p1[1] >= p2[1]

def overlaps(p1, p2):
    # https://stackoverflow.com/a/3269471/193886
    # x1 <= y2 && y1 <= x2
    return p1[0] <= p2[1] and p2[0] <= p1[1]

def parse_line(line):
    m = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
    p1 = int(m.group(1)), int(m.group(2))
    p2 = int(m.group(3)), int(m.group(4))
    return (p1, p2)


def f1(pairs):
    total = 0
    for p1, p2 in pairs:
        total += bool(contains(p1, p2) or contains(p2, p1))
    print(total)

def f2(pairs):
    total = 0
    for p1, p2 in pairs:
        total += overlaps(p1, p2)
    print(total)
