import re
from operator import or_, and_, xor
from itertools import chain

regex = re.compile(r"(\w+) (\w+) (\w+) -> (\w+)")
OPS = {"OR": or_, "AND": and_, "XOR": xor}


def parse(inp):
    nodes = {}
    graph = []
    start, wires = inp.strip().split('\n\n')
    for line in start.splitlines():
        s, boolean = line.split(": ")
        nodes[s] = boolean == '1'
    for line in wires.splitlines():
        graph.append(regex.match(line).groups())

    return nodes, graph


def f1(inp):
    nodes, graph = inp
    all_nodes = {*nodes, *chain.from_iterable([a,b,target] for a, op, b, target in graph)}

    while len(nodes) < len(all_nodes):
        for a, op, b, target in graph:
            if target not in nodes and a in nodes and b in nodes:
                nodes[target] = OPS[op](nodes[a], nodes[b])
    keys = reversed(sorted(a for a in all_nodes if a.startswith('z')))
    return int("".join("1" if nodes[key] else "0" for key in keys), 2)


def f2(inp):
    nodes, graph = inp
    all_nodes = {*nodes, *chain.from_iterable([a, b, target] for a, op, b, target in graph)}
    z_max = max(n for n in all_nodes if n[0] == "z")

    # Look at the errors, there is a structure, back-propagate the errors, we don't try to fix it.
    # Just determine the fixable errors...
    errors = set()

    def subsearch_for_target_ops(target, ops):
        for a, op, b, _ in graph:
            if target in (a, b) and op in ops:
                errors.add(target)

    for a, op, b, target in graph:
        if target[0] == "z" and op != "XOR" and target != z_max:
            errors.add(target)
        elif op == "XOR":
            if all(n[0] not in "xyz" for n in (a, b, target)):
                errors.add(target)
            subsearch_for_target_ops(target, ["OR"])
        elif op == "AND" and "x00" not in (a, b):
            subsearch_for_target_ops(target, ["XOR", "AND"])
    return ",".join(sorted(errors))
