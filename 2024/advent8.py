from collections import defaultdict
from itertools import combinations
from math import gcd

from util import BaseBoard


class Board(BaseBoard):
    def __init__(self, input):
        super().__init__(input)
        self.nodes = defaultdict(list)
        for y, row in enumerate(self.board):
            for x, char in enumerate(row):
                if char == '.':
                    continue
                self.nodes[char].append((x, y))

    def unique_antinodes(self):
        result = set()

        def add(x, y):
            if 0 <= x < self.width and 0 <= y < self.height:
                result.add((x, y))

        for key, nodes in self.nodes.items():
            # print(key, nodes)
            for n1, n2 in combinations(nodes, 2):
                dx, dy = n2[0] - n1[0], n2[1] - n1[1]
                add(n1[0] - dx, n1[1] - dy)
                add(n2[0] + dx, n2[1] + dy)

        return result

    def unique_antinodes2(self):
        result = set()

        for key, nodes in self.nodes.items():
            for n1, n2 in combinations(nodes, 2):
                dx, dy = n2[0] - n1[0], n2[1] - n1[1]
                factor = gcd(dx, dy)
                dx /= factor
                dy /= factor

                x, y = n1
                while 0 <= x < self.width and 0 <= y < self.height:
                    result.add((x, y))
                    x += dx
                    y += dy

                x, y = n1
                while 0 <= x < self.width and 0 <= y < self.height:
                    result.add((x, y))
                    x -= dx
                    y -= dy

        return result


def parse(input):
    return Board(input.split("\n"))


def f1(board):
    return len(board.unique_antinodes())


def f2(board):
    return len(board.unique_antinodes2())
