from itertools import pairwise


def parse_line(line):
    return [int(i) for i in line.split(" ")]


def calc(lst: list[int]):
    result = lst[-1]
    while not (all(l == 0 for l in lst)):
        lst = [b - a for a, b in pairwise(lst)]
        result += lst[-1]
    return result


def f1(input):
    return sum(calc(i) for i in input)


def calc2(lst: list[int]):
    results = lst[:1]
    while not (all(l == 0 for l in lst)):
        lst = [b - a for a, b in pairwise(lst)]
        results.append(lst[0])
    results.reverse()

    result = 0
    for i in results:
        result = i - result
    return result


def f2(input):
    # calc2([10, 13, 16, 21, 30, 45])
    return sum(calc2(i) for i in input)
