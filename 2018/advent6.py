import operator
from collections import deque
from dataclasses import dataclass

from util import HV_VARIANTS


@dataclass
class Block:
    index: int | None
    depth: int

    def __str__(self) -> str:
        if self.index is None:
            return "."
        base = ord("A" if self.depth == 0 else "a")
        return chr(base + self.index)


class Board:
    def __init__(self, input):
        self.items = []
        width = height = 0
        for line in input:
            x, y = map(int, line.split(", "))
            self.items.append((x, y))
            if x + 1 > width:
                width = x + 1
            if y + 1 > height:
                height = y + 1
        self.infinite: list[bool] = [False] * len(self.items)
        self.width = width
        self.height = height
        self.board: list[list[Block | None]] = [[None] * width for _ in range(height)]
        for index, (x, y) in enumerate(self.items):
            self.board[y][x] = Block(index, 0)

    def __str__(self):
        return "\n".join(
            "".join(str(e) if e else "." for e in row) for row in self.board
        )

    def breadth_first(self):
        q = deque()
        for x in self.items:
            q.append(x)
        while len(q):
            x, y = q.popleft()
            node = self.board[y][x]
            for dx, dy in HV_VARIANTS:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    if node.index is not None:
                        self.infinite[node.index] = True
                    continue
                nnode, n_depth = self.board[ny][nx], node.depth + 1
                if nnode is None:
                    self.board[ny][nx] = Block(node.index, depth=n_depth)
                    q.append((nx, ny))
                    continue
                assert nnode.depth <= n_depth
                if nnode.depth < n_depth:
                    continue
                if nnode.index in (node.index, None):
                    continue
                nnode.index = None

    def area_per_item(self):
        result = [0] * len(self.items)
        for row in self.board:
            for node in row:
                if node.index is not None:
                    result[node.index] += 1
        return result


def f1(input):
    board = Board(input)
    board.breadth_first()
    area_per_item = board.area_per_item()
    index, area = max(
        (p for p in enumerate(area_per_item) if not board.infinite[p[0]]),
        key=operator.itemgetter(1),
    )
    return chr(ord("A") + index), area
