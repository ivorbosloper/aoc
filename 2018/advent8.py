from dataclasses import dataclass
from typing import Iterator, List


@dataclass
class Node:
    children: List["Node"]
    metadata: List[int]
    _value: int | None = None

    def __iter__(self):
        yield self
        for c in self.children:
            yield from c

    @property
    def value(self) -> int:
        if self._value is None:
            if len(self.children):
                self._value = 0
                for index in self.metadata:
                    if index <= len(self.children):
                        self._value += self.children[index - 1].value
            else:
                self._value = sum(self.metadata, 0)
        return self._value


def parse_i(input: Iterator[int]) -> Node:
    nr_children = next(input)
    nr_meta = next(input)
    children = [parse_i(input) for _ in range(nr_children)]
    metadata = [next(input) for _ in range(nr_meta)]
    return Node(children, metadata)


def parse(input) -> Node:
    return parse_i(map(int, input.split(" ")))


def f1(root: Node):
    return sum(sum(node.metadata, 0) for node in root)


def f2(root: Node):
    return root.value
