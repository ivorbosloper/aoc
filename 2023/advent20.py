import math
from dataclasses import dataclass, field
from enum import Enum


class NType(Enum):
    BC = 1
    XOR = 2
    AND = 3


@dataclass
class Node:
    name: str
    connections: list[str] = field(default_factory=list)


@dataclass
class FlipFlopNode(Node):
    state: bool = False


@dataclass
class ConjunctionNode(Node):
    incoming: dict[str, bool] = field(default_factory=dict)


class Machine:
    def __init__(self, input) -> None:
        # start, end, pulse
        self.sent = [0, 0]
        self.signals: list[tuple[str, str, bool]] = []
        self.nodes: dict[str, Node] = {}
        for line in input:
            name, b = line.split(" -> ")
            connections = b.split(", ")
            if name == "broadcaster":
                node = Node(name, connections=connections)
            else:
                t, name = name[0], name[1:]
                if t == "%":
                    node = FlipFlopNode(name, connections=connections)
                else:
                    node = ConjunctionNode(name, connections=connections)
            self.nodes[name] = node
        for name, node in self.nodes.items():
            for c in node.connections:
                target = self.nodes.get(c)
                if isinstance(target, ConjunctionNode):
                    target.incoming[name] = False

    def report(self):
        for start, end, pulse in self.signals:
            self.sent[pulse] += 1

    def simulate(self):
        nsignals: list[tuple[str, str, bool]] = []
        self.report()
        for start, end, pulse in self.signals:
            # print(f"{start} -{'high' if pulse else 'low'}-> {end}")
            node = self.nodes.get(end)
            if node is None:
                continue
            if node.__class__ == Node:
                # for broadcaster, send pulse to connections
                pass
            elif isinstance(node, FlipFlopNode):
                if pulse:
                    continue  # high pulse --> do nothing
                # low pulse: flip bit and send to connections
                pulse = node.state = not node.state
            elif isinstance(node, ConjunctionNode):
                node.incoming[start] = pulse
                pulse = not all(node.incoming.values())

            for c in node.connections:
                nsignals.append((end, c, pulse))

        self.signals = nsignals
        return len(nsignals) > 0

    def push_button(self):
        assert len(self.signals) == 0
        self.signals.append(("button", "broadcaster", False))
        while self.simulate():
            pass
        # print(f"sent so far {self.sent}")


def f1(input):
    m = Machine(input)
    for _ in range(1000):
        m.push_button()
    return math.prod(m.sent)


class Machine2(Machine):
    signal_count = {}
    bit_flips = {}
    turn = 0

    def report(self):
        sc = self.signal_count
        for start, end, pulse in self.signals:
            if end not in sc:
                continue
            if end not in self.bit_flips:
                self.bit_flips[end] = (self.turn, pulse)
                continue
            elif self.bit_flips[end][1] == pulse:
                continue
            new_turns = self.turn - self.bit_flips[end][0]
            if new_turns == 0:
                if pulse != self.bit_flips[end][1]:
                    self.bit_flips[end] = (self.turn, pulse)
                continue

            # print(f"Found {end} {self.turn}")
            sc[end] = new_turns
            self.bit_flips[end] = (self.turn, pulse)


def f2(input):
    m = Machine2(input)
    if "pr" not in m.nodes:
        return
    final_nodes = set(n.name for n in m.nodes.values() if "rx" in n.connections)
    assert len(final_nodes) == 1
    final_node = m.nodes[final_nodes.pop()]
    m.signal_count = {k: 0 for k in final_node.incoming}  # type: ignore

    # 10000 is enough to find the cycle-length
    # First occurence of cycle is:
    # {'jg': 3792, 'rh': 4018, 'jm': 4002, 'hf': 3946}
    #
    # However, cycle length can only be found by continuing up at least 4019 * 2:
    # {'jg': 3793, 'rh': 4019, 'jm': 4003, 'hf': 3947}
    while m.turn < 10000:
        m.push_button()
        m.turn += 1
    print(m.signal_count)
    # 10025387884848 too low, I forgot to cycle
    print(math.lcm(*list(m.signal_count.values())))
