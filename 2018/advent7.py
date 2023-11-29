from ast import Set
from collections import defaultdict, namedtuple
from copy import deepcopy
from typing import NamedTuple

from numpy import char


def parse(input) -> dict:
    graph = defaultdict(set)
    for line in input.split("\n"):
        graph[line[36]].add(line[5])
        graph[line[5]]
    return graph


def graph_iter(graph):
    while len(graph):
        candidate = min(node for node, links in graph.items() if len(links) == 0)
        del graph[candidate]
        for node, links in graph.items():
            links.discard(candidate)
        yield candidate


def f1(input):
    graph = deepcopy(input)
    return "".join(graph_iter(graph))


def f2(input):
    if len(input) < 10:
        nr_workers, work_time = 2, 1
    else:
        nr_workers, work_time = 5, 61

    result = []
    graph = deepcopy(input)
    work: dict[str, int] = {}
    second = 0
    while work or graph:
        while len(work) < nr_workers:
            # print(second, len(graph), work)
            candidates = [
                node
                for node, links in graph.items()
                if len(links) == 0 and node not in work
            ]
            if len(candidates) == 0:
                break
            candidate = min(candidates)
            work[candidate] = second + work_time + ord(candidate) - ord("A")

        second += 1
        removals = [node for node, finish in work.items() if finish == second]
        for node in removals:
            # print(f"removing {node} at second {second}")
            result.append(node)
            del work[node]
            del graph[node]
            for links in graph.values():
                links.discard(node)

    return second, "".join(result)
