import re
import math
from collections import defaultdict
from functools import cached_property
from typing import Optional

M = {'#': "1", '.': "0"}
TOP, RIGHT, BOTTOM, LEFT = [0, 1, 2, 3]  # ROWS; TOP, RIGHT, BOTTOM, LEFT
REVERSED = {i: int(f"{i:010b}"[::-1], 2) for i in range(1024)}
TILE, VARIANT = 0, 1

def int_hash(s):
    return int("".join(M[c] for c in s), 2)


class Tile:
    def __init__(self, input):
        self.nr = int(re.match(r"Tile (\d+):", input[0]).group(1))
        self.tile = input[1:]
        # Top, right, bottom, left. Value in clockwise direction
        self.sides = (int_hash(self.tile[0]), int_hash(row[-1] for row in self.tile),
                      REVERSED[int_hash(self.tile[-1])], REVERSED[int_hash(row[0] for row in self.tile)])


    @cached_property
    def variants(self):
        # 8 different bits. Only one flip required
        b = self.sides
        flipped_y = (b[2], REVERSED[b[1]], b[0], REVERSED[b[3]])
        return tuple((b[i:] + b[:i]) for i in range(4)) + \
               tuple((flipped_y[i:] + flipped_y[:i]) for i in range(4))

    def __hash__(self):
        return self.nr


def parse(input):
    return [Tile(i.split('\n')) for i in input.split("\n\n")]

def vtostr(variant):
    print([f"{i:010b}" for i in to_try[index - size][pointer[index - size]][VARIANT]])

def f1(tiles):
    size = int(math.sqrt(len(tiles)))

    for v in tiles[0].variants:
        print(vtostr(v))
    return

    if size > 3 : return

    to_try = [None for _ in tiles]  # List of List[(Tile, variant)]
    pointer = [-1 for _ in tiles]   # Counter in index
    index = 0
    while True:  # index >= 0:
        y, x = index // size, index % size
        print([to_try[i][pointer[i]][TILE].nr for i in range(index)])
        if to_try[index] is None:
            used_tiles = [to_try[i][pointer[i]][TILE] for i in range(index)]
            check_left = REVERSED[to_try[index - 1][pointer[index - 1]][VARIANT][RIGHT]] if x > 0 else None
            check_top = REVERSED[to_try[index - size][pointer[index - size]][VARIANT][BOTTOM]] if y > 0 else None
            new_options = []
            if [to_try[i][pointer[i]][0].nr for i in range(index)] == [1951, 2311, 3079]: breakpoint()
            for t in tiles:
                if t in used_tiles:
                    continue
                for v in t.variants:
                    if check_left and check_left != v[LEFT]:
                        continue
                    if check_top and check_top != v[TOP]:
                        continue
                    new_options.append((t, v))

            to_try[index] = new_options
            new_pointer = 0
        else:
            new_pointer = pointer[index] + 1
        while new_pointer >= len(to_try[index]):  # if we overshoot, take a step back
            to_try[index] = None
            if index == 0: return
            index -= 1
            new_pointer = pointer[index] + 1
        pointer[index] = new_pointer
        if index == len(tiles):
            print("SOLVED", [to_try[i][pointer[i]][0].nr for i in range(index)])
        else:
            index += 1
