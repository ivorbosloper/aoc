from collections import defaultdict

parse_line = int


def f1(input):
    input.sort()
    prev = 0
    diffs = defaultdict(int)
    diffs[3] = 1  # last step
    for i in input:
        diffs[i-prev] += 1
        prev = i

    return diffs[1] * diffs[3]


def f1(input):
    input.sort()
    ways_to_reach = [0 for _ in range(input[-1]+3)]
    ways_to_reach[0] = 1
    for i in input:
        for j in range(1, 4):
            if i-j >= 0:
                ways_to_reach[i] += ways_to_reach[i-j]

    print(ways_to_reach[input[-1]], ways_to_reach)
