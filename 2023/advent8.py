import math

Graph = dict[str, tuple]


def parse(input):
    lines = input.split("\n")

    graph: Graph = {}
    for line in lines[2:]:
        start, left, right = line[:3], line[7:10], line[12:15]
        graph[start] = left, right

    return lines[0], graph


def f1(input):
    line, graph = input
    return
    i = -1
    steps = 0
    current = "AAA"
    while current != "ZZZ":
        steps += 1
        i = (i + 1) % len(line)
        current = graph[current][0 if line[i] == "L" else 1]
    return steps


def f2(input):
    line, graph = input
    if len(line) < 3:
        return

    # emulate until you found all cycles.
    # then, if you found a cycles, you should create a list dist-to next-a
    # then each round, take the largest jump you can take (first opportunity for having all-a)

    # It's even easier. The cycles are all simple; they start at a cycle (step 0 is the first in-step).
    # And the pattern repeats at every cycle too
    # This program is not a general solution, it only works for my given input.
    # The lengths of the found loops were all divisible by the LR-line-length
    # I found this only by writing a more complex program, and discovering it was not required for this input

    current = [a for a in graph if a[2] == "A"]
    lens = []
    # while not all(c[2] == "Z" for c in current):  naive approach, too slow
    for i in range(len(current)):
        steps = 0
        while current[i][2] != "Z":
            LR = 0 if line[steps % len(line)] == "L" else 1
            current[i] = graph[current[i]][LR]
            steps += 1
        assert steps % len(line) == 0
        lens.append(steps)

    # not GCD of LCM
    return math.lcm(*lens)
    # 11_795_205_644_011
