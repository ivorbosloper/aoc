import itertools
import operator
import sys
from graphlib import TopologicalSorter

EMPTY = tuple()


def parse(input):
    a, b = input.split("\n\n")
    rules = [tuple(map(int, line.split('|'))) for line in a.split("\n")]
    lines = [tuple(map(int, line.split(','))) for line in b.split("\n")]
    return rules, lines


def is_topo_sorted(line, graph):
    location = {v: i for i, v in enumerate(line)}
    for i, num in enumerate(line):
        check = graph.get(num, EMPTY)
        for c in check:
            # print(f'checking {i} loc({num}) < loc({c}): {i < location.get(c, sys.maxsize)}')
            if not i < location.get(c, sys.maxsize):
                return False
    return True


def f1(input):
    rules, lines = input
    before = {key: tuple(g[1] for g in group) for key, group in itertools.groupby(sorted(rules), operator.itemgetter(0))}
    return sum(line[len(line) // 2] for line in lines if is_topo_sorted(line, before))


def f2(input):
    rules, lines = input
    before = {key: tuple(g[1] for g in group) for key, group in itertools.groupby(sorted(rules), operator.itemgetter(0))}
    total = 0
    for line in lines:
        if is_topo_sorted(line, before):
            continue
        line = set(line)
        graph = {key: (g for g in group if g in line) for key, group in before.items() if key in line}
        ts = TopologicalSorter(graph)
        # list should be reversed, but middle element is the same
        total += tuple(ts.static_order())[len(line) // 2]
    return total
