import math
import operator
import re
import sys
from functools import cached_property, reduce
from typing import Annotated, Any, NamedTuple, Tuple


class Outer(NamedTuple):
    top: int
    right: int
    bottom: int
    left: int



M = {'#': "1", '.': "0"}
REVERSED = {i: int(f"{i:010b}"[::-1], 2) for i in range(1024)}
TILE, VARIANT = 0, 1

def int_hash(s: str) -> int:
    return int("".join(M[c] for c in s), 2)


class Tile:
    def __init__(self, input):
        self.nr: int = int(re.match(r"Tile (\d+):", input[0]).group(1))
        self.tile: str[10] = input[1:]
        # Top, right, bottom, left. Values in left2right, top2bottom direction
        self.sides: Outer = Outer(
            int_hash(self.tile[0]),
            int_hash(row[-1] for row in self.tile),
            int_hash(self.tile[-1]),
            int_hash(row[0] for row in self.tile)
        )


    @classmethod
    def rotations(clazz, sides: Outer) -> Annotated[Tuple[Outer], 4]:
        b = sides
        result = [sides]
        for _ in range(3):
            b = Outer(REVERSED[b.left], b.top, REVERSED[b.right], b.bottom)
            result.append(b)
        return tuple(result)

    @cached_property
    def variants(self) -> Annotated[Tuple[Outer], 8]:
        b = self.sides
        flipped_y = Outer(b.bottom, REVERSED[b.right], b.top, REVERSED[b.left])
        return Tile.rotations(b) + Tile.rotations(flipped_y)

    def image(self, rotation: int):
        tile = self.tile
        if rotation >= 4:
            rotation -= 4
            tile = list(reversed(tile))
        for _ in range(rotation):
            tile = [
                "".join(tile[8-x][y] for x in range(9)) for y in range(9)
            ]
        assert(all(len(line) == 9 for line in tile))
        return tile


class Board:
    def __init__(self, tiles) -> None:
        self.tiles = tiles
        nr_tiles = len(tiles)
        self.nr_tiles = nr_tiles
        self.size = int(math.sqrt(nr_tiles))
        self.board: list[int] = [-1] * nr_tiles
        self.rotation: list[int] = [-1] * nr_tiles

    def print(self):
        for i in range(self.nr_tiles):
            if i>0 and i % self.size == 0: print("")
            sys.stdout.write(f"{self.tiles[self.board[i]].nr} ")
        print("\n")

    def tile(self, index):
        return self.tiles[self.board[index]]

    def outer(self, index):
        return self.tile(index).variants[self.rotation[index]]

    def solve(self):
        used_tiles = [False] * self.nr_tiles
        index = 0
        while True:  # index >= 0, board+rotation[0...index-1] fit 
            if index >= self.nr_tiles:
                print("SOLVED")
                self.print()
                result = reduce(operator.mul, (self.tile(index).nr for index in 
                        (0, self.size-1, self.nr_tiles - self.size, self.nr_tiles-1)), 1)
                return result
            # doe een stap, alleen als het mag, verhoog de index en ander doorloopen

            # elke loop board[index] een tile of een rotatie doorschuiven
            # print(index, self.board[index], self.rotation[index])
            assert sum(used_tiles) == index
            if self.board[index] == -1:
                self.board[index] = next(i for i in range(self.nr_tiles) if not used_tiles[i])
                self.rotation[index] = 0
            else:
                self.rotation[index] += 1

            # print(self.tile(index).image(self.rotation[index]))
            y, x = index // self.size, index % self.size
            while self.rotation[index] < 8:
                v = self.outer(index)
                if (x > 0 and self.outer(index-1).right != v.left) or \
                   (y > 0 and self.outer(index-self.size).bottom != v.top):
                    self.rotation[index] += 1
                    continue

                break # it fits

            if self.rotation[index] < 8:
                used_tiles[self.board[index]] = True
                index += 1
                if index < self.nr_tiles:
                    self.board[index] = -1
                continue

            nxt = next((i for i in range(self.board[index]+1, self.nr_tiles) if not used_tiles[i]), None)
            if nxt is not None:
                self.board[index] = nxt
                self.rotation[index] = -1
                continue

            if index == 0:
                return print("UNSOLVED")
            index -= 1
            used_tiles[self.board[index]] = False


def parse(input):
    return [Tile(i.split('\n')) for i in input.split("\n\n")]

def vtostr(variant):
    print(variant[0])

def f1(tiles):
    board = Board(tiles)
    return board.solve()


class Board2(Board):
    def print(self):
        pass

    def solve(self):
        super().solve()
        images = [self.tile(index).image(self.rotation[index]) for index in range(self.nr_tiles)]
        image = sum([
                ["".join(
                    [images[y*self.size + x][line] for x in range(self.size)])
                 for line in range(8)]
               for y in range(self.size)
        ], [])
        print("\n".join(image))


def f2(tiles):
    board = Board2(tiles)
    board.solve()
