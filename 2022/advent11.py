from io import StringIO
import operator
from functools import reduce
import copy

def parse(input):
    monkeys = []
    for _lines in input.split("\n\n"):
        lines = _lines.split('\n')
        op_arg = lines[2][len('  Operation: new = old '):].split(' ')
        m = dict(
            items=[int(s.strip()) for s in lines[1][len('  Starting items: '):].split(',')],
            op=operator.add if op_arg[0] == '+' else operator.mul,
            arg=int(op_arg[1]) if op_arg[1].isdigit() else op_arg[1],
            divider=int(lines[3][len('  Test: divisible by '):]),
            left=int(lines[4][len('    If true: throw to monkey ')]),
            right=int(lines[5][len('    If false: throw to monkey ')]),
            inspections=0
        )
        assert len(monkeys) not in (m['left'], m['right'])
        monkeys.append(m)
    return monkeys


def apply_op(monkey, v):
    return 


def f1(monkeys):
    monkeys = copy.deepcopy(monkeys)
    for _ in range(20):
        for monkey in monkeys:
            monkey['inspections'] += len(monkey['items'])
            for v in monkey['items']:
                item = monkey['op'](v, v if monkey['arg'] == 'old' else monkey['arg']) // 3 
                monkeys[monkey["left" if item % monkey['divider'] == 0 else "right"]]["items"].append(item)
            monkey['items'] = []
        # print(f"Round {_}")
        # for index, monkey in enumerate(monkeys):
        #     print(f"Monkey {index} inspected items {monkey['inspections']} times.")
        # print()
            
        # for index, monkey in enumerate(monkeys):
        #     print(f"Monkey {index}: {', '.join(map(str, monkey['items']))}")
        # print()

    # for index, monkey in enumerate(monkeys):
    #     print(f"Monkey {index} inspected items {monkey['inspections']} times.")
    srt = sorted(m['inspections'] for m in monkeys)
    print(srt[-1] * srt[-2])


def f2(monkeys):
    # only change is; 10000 ops, don't div 3 but modulo by multiplied dividers (as this won't affect the outcome)
    monkeys = copy.deepcopy(monkeys)
    for _ in range(10000):
        total = reduce(operator.mul, [monkey['divider'] for monkey in monkeys])
        for monkey in monkeys:
            monkey['inspections'] += len(monkey['items'])
            for v in monkey['items']:
                item = monkey['op'](v, v if monkey['arg'] == 'old' else monkey['arg']) % total
                monkeys[monkey["left" if item % monkey['divider'] == 0 else "right"]]["items"].append(item)
            monkey['items'] = []
    srt = sorted(m['inspections'] for m in monkeys)
    print(srt[-1] * srt[-2])
