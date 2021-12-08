import sys
from collections import defaultdict


def parse(input):
    return [int(i) for i in input.split(",")]


def calc(input, cost):
    count_per_position = defaultdict(int)
    for c in input:
        count_per_position[c] += 1

    min_dist = sys.maxsize
    for target in range(min(input), max(input)):
        dist = sum(cost(abs(nr - target)) * count for nr, count in count_per_position.items())
        if dist < min_dist:
            min_dist = dist
    return min_dist


def f1(input):
    return calc(input, lambda x:x)


def f2(input):
    cost_array = [0]
    for i in range(1, max(input)+1):
        cost_array.append(cost_array[i-1] + i)
    return calc(input, lambda x: cost_array[x])
