from collections import defaultdict
from itertools import groupby


def parse(inp):
    return [int(i) for i in inp.split(" ")]


def f1(line):
    for i in range(25):
        nline = []
        for nr in line:
            if nr == 0:
                nline.append(1)
            elif len(s := str(nr)) % 2 == 0:  # int(math.log10(100)) % 2:
                nline.append(int(s[:len(s)//2]))
                nline.append(int(s[len(s)//2:]))
            else:
                nline.append(nr * 2024)
        line = nline
    return len(line)


# work with histograms, {5: 3, 12: 30} means [5,5,5,12,12,12...]. Order is irrelevant
def f2(line):
    line = {key: sum(1 for _ in group) for key, group in groupby(sorted(line))}
    for i in range(75):
        nline = defaultdict(int)
        for nr, amount in line.items():
            if nr == 0:
                nline[1] += amount
            elif len(s := str(nr)) % 2 == 0:
                nline[int(s[:len(s)//2])] += amount
                nline[int(s[len(s)//2:])] += amount
            else:
                nline[nr * 2024] += amount
        line = nline
    return sum(line.values())
