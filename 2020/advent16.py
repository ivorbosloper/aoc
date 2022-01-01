import operator
import re
from functools import reduce

re_rule = re.compile(r"([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)")


# class MultiRange:
#     def __init__(self, *args):
#         assert len(args) % 2 == 0
#         self.ranges = [range(args[i], args[i+1]) for i in range(0, len(args), 2)]
#
#     def __contains__(self, item):
#         return any(item in r for r in self.ranges)

def merge_ranges(*args):
    i, result = 0, set()
    while i < len(args):
        if isinstance(args[i], int):
            result.update(range(args[i], args[i+1]))
            i += 2
            continue
        result.update(args[i])
        i += 1
    return result


def parse(input):
    parts = [block.split("\n") for block in input.split("\n\n")]
    return (
        {a[0]: merge_ranges(*(int(nr)+i % 2 for i, nr in enumerate(a[1:]))) for a in [re_rule.match(line).groups() for line in parts[0]]},
        [int(i) for i in parts[1][1].split(',')],
        [[int(i) for i in line.split(',')] for line in parts[2][1:]]
    )


def f1(parts):
    rules, own, others = parts
    all_rule = merge_ranges(*rules.values())
    return sum(nr for o in others for nr in o if nr not in all_rule)


def f2(parts):
    rules, own, others = parts
    all_rule = merge_ranges(*rules.values())
    length = len(own)

    valid_others = [line for line in others if all(nr in all_rule for nr in line)]
    if len(valid_others) < 4: return 0
    r_mapping = {name: [all(line[i] in rule for line in valid_others) for i in range(length)] for name, rule in rules.items()}
    mapping = {}  # class --> index
    while len(mapping) < len(r_mapping):
        leftover = [i for i in range(length) if i not in mapping.values()]
        new_m = {key: [i for i in leftover if valids[i]] for key, valids in r_mapping.items()}
        new_1 = {key: v[0] for key, v in new_m.items() if len(v) == 1}
        assert len(new_1)
        mapping.update(new_1)

    departure_values = [own[v] for k, v in mapping.items() if k.startswith('departure')]
    assert len(departure_values) == 6
    return reduce(operator.mul, departure_values)
