import math
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from operator import gt, lt

Instr = tuple[int, int, int, int]
Range = tuple[int, int]
IRange = tuple[Range, Range, Range, Range]
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
            for rule in self.rules[state]:
                if isinstance(rule, str):
                    state = rule
                    break
                if m := rule.operate(instr):
                    state = m
                    break

        return state == "A"

    def valid_states(self, state, space: IRange):
        content = math.prod([b - a for a, b in space])
        assert content > 0
        if state in ("R", "A"):
            return content if state == "A" else 0
        result = 0
        for rule in self.rules[state]:
            if isinstance(rule, str):
                result += self.valid_states(rule, space)
                break

            vi = "xmas".index(rule.arg)
            vr = space[vi]
            if rule.op == "<":
                r_if = vr[0], min(rule.val, vr[1])
                r_else = max(rule.val, vr[0]), vr[1]
            else:
                r_if = max(rule.val + 1, vr[0]), vr[1]
                r_else = vr[0], min(rule.val + 1, vr[1])

            if r_if[1] - r_if[0] > 0:
                r_space = tuple(r_if if i == vi else r for i, r in enumerate(space))
                result += self.valid_states(rule.label, r_space)  # type: ignore
            if r_else[1] - r_else[0] <= 0:
                break  # do not continue, space left is empty
            space = tuple(r_else if i == vi else r for i, r in enumerate(space))  # type: ignore

        return result


def parse(input):
    return Machine(input)


def f1(machine):
    return sum(sum(i) for i in machine.instrs if machine.exec(i))


def f2(machine):
    return machine.valid_states("in", tuple((1, 4001) for _ in range(4)))
