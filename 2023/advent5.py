from collections import defaultdict
from curses import nl
from typing import NamedTuple

try:
    from itertools import batched  # type: ignore
except ImportError:
    from itertools import islice

    def batched(iterable, n):
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield batch


class Graph:
    def __init__(self, input):
        self.start: list[int] = []
        sections = [i.split("\n") for i in input.split("\n\n")]

        self.connections: list[list[tuple]] = []
        # seed-to-soil map:
        for index, section in enumerate(sections):
            if index == 0:
                assert section[0].startswith("seeds: ")
                self.start = [int(x) for x in section[0][7:].split(" ")]
                continue

            lst = []
            self.connections.append(lst)

            for line in section[1:]:
                trange, srange, length = map(int, line.split(" "))
                lst.append((srange, trange, length))
            lst.sort()

    def map(self, nr):
        for conlist in self.connections:
            for srange, trange, length in conlist:
                if srange <= nr < srange + length:
                    nr = nr - srange + trange
                    break
        return nr

    def map_ranges(self, ranges):
        rnext = ranges = ranges[::]
        for conlist in self.connections:
            rnext = []
            for rng in ranges:
                range = rng
                for srange, trange, length in conlist:
                    if srange + length < range[0]:
                        continue  # not in reach yet
                    if sum(range) < srange:
                        break  # past all options
                    # 1. cut part before and push in result
                    cut_off = srange - range[0]
                    if cut_off > 0:
                        rnext.append((range[0], cut_off))
                        range = range[0] + cut_off, range[1] - cut_off
                        if range[1] == 0:
                            break  # processed the whole range
                        assert range[1] > 0

                    # 2. cut overlapping, map and push in result
                    start, end = max(srange, range[0]), min(srange + length, sum(range))
                    nlength = end - start
                    assert nlength >= 0
                    if nlength > 0:
                        rnext.append((start + trange - srange, nlength))
                        range = end, range[1] - nlength

                    # 3. continue if range.len > 0
                    if range[1] == 0:
                        break
                if range[1] > 0:
                    # non-processable part continues to next round
                    rnext.append(range)
            ranges = rnext
        return rnext


def parse(input):
    return Graph(input)


def f1(graph):
    return min(graph.map(x) for x in graph.start)


def f2(graph):
    ranges = list(batched(graph.start, 2))
    return min(m[0] for m in graph.map_ranges(ranges))
