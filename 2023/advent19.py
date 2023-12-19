import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from operator import gt, lt

Instr = tuple[int, int, int, int]
OPS = {"<": lt, ">": gt}


@dataclass
class JumpIf:
    arg: str
    op: str
    val: int
    label: str

    def operate(self, instr: Instr):
        v = instr["xmas".index(self.arg)]
        if OPS[self.op](v, self.val):
            return self.label


Rule = JumpIf | str


class Machine:
    rules: dict[str, list[Rule]]
    instrs: list[Instr]

    def __init__(self, input: str) -> None:
        self.rules = defaultdict(list)
        p1, p2 = (p.split("\n") for p in input.split("\n\n"))
        for line in p1:
            assert (m := re.match(r"(\w+)\{(.*)\}", line))
            name, rest = m.groups()
            for r in rest.split(","):
                if m := re.match(r"([xmas])([<>])(\d+):(\w+)", r):
                    self.rules[name].append(
                        JumpIf(m.group(1), m.group(2), int(m.group(3)), m.group(4))
                    )
                else:
                    assert re.match(r"\w+", r)
                    self.rules[name].append(r)

        self.instrs = []
        for line in p2:
            assert (m := re.match(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", line))
            self.instrs.append(tuple(int(p) for p in m.groups()))  # type: ignore

    def exec(self, instr):
        state = "in"
        while not state in ("R", "A"):
            print(state, self.rules[state])
            for rule in self.rules[state]:
                if isinstance(rule, str):
                    state = rule
                    break
                if m := rule.operate(instr):
                    state = m
                    break

        return state == "A"


def parse(input):
    return Machine(input)


def f1(machine):
    return sum(sum(i) for i in machine.instrs if machine.exec(i))


def f2(machine):
    pass
