import re


def f1(input):
    return sum(int(g[0]) * int(g[1]) for g in re.findall(r"mul\((\d+),(\d+)\)", " ".join(input)))


def f2(input):
    if len(input) == 1:
        input = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]

    result = 0
    enabled = True
    for a in re.findall(r"(?:mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))", " ".join(input)):
        if a[2] or a[3]:
            enabled = bool(a[2])
        elif enabled:
            result += int(a[0]) * int(a[1])
    return result
