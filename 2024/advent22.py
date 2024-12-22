from collections import defaultdict


def calc(nr):
    nr = (nr ^ (nr << 6)) & 16777215
    nr = nr ^ (nr >> 5)
    return (nr ^ (nr << 11)) & 16777215


def f1(inp):
    total = 0
    for nr in inp:
        nr = int(nr)
        for i in range(2000):
            nr = calc(nr)
        total += nr
    return total


def f2(inp):
    deltas = []
    digits = []
    for nr in inp:
        nr = int(nr)
        prev = nr % 10
        deltas.append([])
        digits.append([])
        nr = int(nr)
        for i in range(2000):
            nr = calc(nr)
            digit = nr % 10
            deltas[-1].append(digit - prev)
            digits[-1].append(digit)
            prev = digit

    sums = defaultdict(int)
    for delta, digit in zip(deltas, digits):
        first = {}
        for i in range(4, 2000):
            first.setdefault(tuple(delta[i-4:i]), digit[i-1])
        for k, v in first.items():
            sums[k] += v

    return max(v for k,v in sums.items())
