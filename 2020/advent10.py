parse_line = int


def f1(input):
    input.sort()
    target = input[-1]
    reachable = [False for _ in range(target)]

