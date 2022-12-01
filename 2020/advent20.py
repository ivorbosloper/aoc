import re
import math
from collections import defaultdict
from functools import cached_property
from typing import Optional

M = {'#': "1", '.': "0"}
TRBL = [0, 1, 2, 3]
FLIPPED = {i: int(f"{i:010b}"[::-1], 2) for i in range(1024)}


def int_hash(s):
    return int("".join(M[c] for c in s), 2)


class Tile:
    def __init__(self, input):
        self.nr = int(re.match(r"Tile (\d+):", input[0]).group(1))
        self.tile = input[1:]
        # Top, right, bottom, left. Value in clockwise direction
        self.bits = (int_hash(self.tile[0]), int_hash(row[-1] for row in self.tile),
                     FLIPPED[int_hash(self.tile[-1])], FLIPPED[int_hash(row[0] for row in self.tile)])

    @cached_property
    def variants(self):
        # 8 different bits. Only one flip required
        b = self.bits
        flipped_y = (b[2], FLIPPED[b[1]], b[0], FLIPPED[b[3]])
        return tuple((b[i:] + b[:i]) for i in range(4)) + \
               tuple((flipped_y[i:] + flipped_y[:i]) for i in range(4))

    def __hash__(self):
        return self.nr


def parse(input):
    return [Tile(i.split('\n')) for i in input.split("\n\n")]


def f1(tiles):
    size = int(math.sqrt(len(tiles)))
    if size > 3 : return
    hash_right, hash_bottom = defaultdict(list), defaultdict(list)
    for tile in tiles:
        for variant in tile.variants:  # trbl
            hash_right[FLIPPED[variant[1]]].append((tile, variant))
            hash_bottom[FLIPPED[variant[2]]].append((tile, variant))

    to_try: list[Optional[(Tile, tuple)]] = [None for _ in tiles]
    pointer = [-1 for _ in tiles]
    index = 0
    while True:  # index >= 0:
        y, x = index // size, index % size
        print([to_try[i][pointer[i]][0].nr for i in range(index)])
        if to_try[index] is None:
            # calculate a new set of options
            prev_tiles = set(to_try[i][pointer[i]][0] for i in range(index))
            filter_left = hash_right[to_try[index - 1][pointer[index - 1]][1][3]] if x > 0 else None
            filter_top = hash_bottom[to_try[index - size][pointer[index - size]][1][0]] if y > 0 else None

            if index == 0:
                new_options = [(t, variant) for t in tiles for variant in t.variants]
            elif x > 0:
                r = set(r[0] for r in filter_top) if filter_top else None
                new_options = [(t, variant) for t, variant in filter_left
                               if t not in prev_tiles and (r is None or t in r)]
            else:  # y>0
                b = set(r[0] for r in filter_left) if filter_left else None
                new_options = [(t, variant) for t, variant in filter_top
                               if t not in prev_tiles and (b is None or t in b)]
            to_try[index] = new_options
            new_pointer = 0
        else:
            new_pointer = pointer[index] + 1
        while new_pointer >= len(to_try[index]):
            to_try[index] = None
            if index == 0: return
            index -= 1
            new_pointer = pointer[index] + 1
        pointer[index] = new_pointer
        if index == len(tiles):
            print("SOLVED", [to_try[i][pointer[i]][0].nr for i in range(index)])
        else:
            index += 1
