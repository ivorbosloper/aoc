from io import StringIO
from graphlib import TopologicalSorter
import operator

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv
}

def parse(input):
    nodes = {}
    values = {}
    graph = {}
    for line in StringIO(input):
        name = line[:4]
        ops = line[6:].strip().split(' ')
        if len(ops) == 1:
            values[name] = int(ops[0])
        else:
            nodes[name] = ops
            graph[name] = {ops[0], ops[2]}
    ts = TopologicalSorter(graph)
    order = tuple(ts.static_order())
    return order, nodes, values, graph

def f1(input):
    order, nodes, values, _ = input

    vs = values.copy()
    for name in order:
        if name not in vs:
            arg1, op, arg2 = nodes[name]
            vs[name] = OPS[op](vs[arg1], vs[arg2])
    return vs['root']

def f2(input):
    order, nodes, values, _ = input
    targets = (nodes['root'][0], nodes['root'][2])

    def expand(name):
        if name == 'humn':
            return "HUMM"
        if vs.get(name) is not None:
            return str(vs[name])
        arg1, op, arg2 = nodes[name]
        return f"({expand(arg1)} {op} {expand(arg2)})"

    vs = values.copy()
    vs['humn'] = None
    for name in order:
        if name not in vs:
            arg1, op, arg2 = nodes[name]
            if vs[arg1] is None or vs[arg2] is None:
                vs[name] = None
            else:
               vs[name] = OPS[op](vs[arg1], vs[arg2])
    # print(expand(targets[0]))
    # print(vs[targets[0]], vs[targets[1]])

    goal = vs[targets[1]]
    pointer = nodes[targets[0]]
    while True:
        arg1, op, arg2 = pointer
        # print(f"{pointer}: {vs.get(arg1)}{op}{vs.get(arg2)} == {goal}")
        arg1_is_value = arg2 =='humn' or vs.get(arg1) is not None
        if arg1_is_value: assert vs.get(arg2) is None
        value = vs[arg1] if arg1_is_value else vs[arg2]
        if op == '*':
            assert goal % value == 0
            goal //= value
        elif op == '+':
            goal -= value
        elif op == '-':
            if arg1_is_value:
                goal = -goal
            goal += value
        elif op == '/':
            if arg1_is_value:
                assert value % goal == 0
                value = value // goal
            else:
                goal *= value
        if 'humn' in (arg1, arg2):
            break
        pointer = nodes[arg2] if arg1_is_value else nodes[arg1]
    return goal

    # try to do the 'reverse', so 8 * x = y --> x = y/8
