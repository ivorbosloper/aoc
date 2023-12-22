import math
from calendar import leapdays
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import pairwise


class Block:
    def __init__(self, line) -> None:
        self.start, self.end = (
            tuple(int(a) for a in _.split(",")) for _ in line.split("~")
        )
        assert all(a <= b for a, b in zip(self.start, self.end))

    @property
    def area(self):
        return math.prod(b - a + 1 for a, b in zip(self.start, self.end))

    @property
    def bottom(self):
        return self.start[2]

    @property
    def top(self):
        return self.end[2]

    def move_down(self, z: int):
        down = self.bottom - z
        assert down >= 0
        self.start, self.end = (
            (v[0], v[1], v[2] - down) for v in (self.start, self.end)
        )

    def overlaps(self, other):
        return all(
            (
                self.start[0] <= other.end[0],
                other.start[0] <= self.end[0],
                self.start[1] <= other.end[1],
                other.start[1] <= self.end[1],
            )
        )

    def __hash__(self) -> int:
        return (self.start + self.end).__hash__()

    def __str__(self):
        return f"Block{self.start} - {self.end}"

    def __repr__(self) -> str:
        return str(self)


parse_line = Block


@dataclass
class Graph:
    blocks: list[Block]
    leans_on: dict[Block, list[Block]] = field(
        default_factory=lambda: defaultdict(list)
    )
    supports: dict[Block, set[Block]] = field(default_factory=lambda: defaultdict(set))

    def collapse(self):
        # make everything fall down
        blocks = self.blocks
        blocks.sort(key=lambda block: block.start[2])
        for index, block in enumerate(blocks):
            if block.bottom == 1:
                continue
            try:
                top = max(b.top for b in blocks[:index] if b.overlaps(block))
            except ValueError:
                top = 0
            if block.bottom != top + 1:
                #  print(f"Moving down {block} from {block.bottom} to {top + 1}")
                block.move_down(top + 1)
        return self

    def connect(self):
        # Make a block --> [block leans on] list(graph)
        # Then, a block that supports block B, and B has no other supporting blocks, is not disintegratable
        blocks = self.blocks
        blocks = sorted(blocks, key=lambda block: block.start[2])
        for index, block in enumerate(blocks):
            for b in blocks[index + 1 :]:
                if block.overlaps(b) and b.bottom == block.top + 1:
                    # print(f"Block {b} leans on {block}")
                    self.leans_on[b].append(block)
                    self.supports[block].add(b)
        return self

    def desintegrations(self, block: Block):
        desintegrated = set([block])
        test = set(self.supports[block])
        while test:
            check = test.pop()
            if check in desintegrated:
                continue
            if not set(self.leans_on[check]).difference(desintegrated):
                desintegrated.add(check)
                test.update(self.supports[check])
        return len(desintegrated) - 1  # minus self


def f1(input):
    assert Block("1,0,1~1,2,1").overlaps(Block("1,0,1~1,2,1"))
    graph = Graph(input)
    graph.collapse().connect()

    free_blocks = set(graph.blocks)
    for b in graph.blocks:
        if len(graph.leans_on[b]) == 1:
            free_blocks.discard(graph.leans_on[b][0])
    return len(free_blocks)


def f2(input):
    graph = Graph(input)
    graph.collapse().connect()

    return sum(graph.desintegrations(block) for block in input)
