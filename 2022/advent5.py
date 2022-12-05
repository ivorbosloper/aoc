from io import StringIO
import re

def parse(input):
    stacks = []
    instructions = None
    for line in StringIO(input):
        line = line[:-1]  # cut \n
        if instructions is not None:
            m = re.match(r"move (\d+) from (\d+) to (\d+)", line)
            instructions.append((int(m.group(1)), int(m.group(2)) - 1, int(m.group(3)) -1))
        elif line == "":
            instructions = []
        else:
            for i, c in enumerate(line):
                if c not in ' []123456789':
                    assert 'A' <= c <= 'Z', 'found ' + c
                    index = i // 4  # 1, 5, 9
                    for j in range(len(stacks), index + 1):
                        stacks.append([])
                    stacks[index].insert(0, c)
    return stacks, instructions

def f1(input):
    stacks, instructions = input
    for amount, source, target in instructions:
        for i in range(amount):
            c = stacks[source].pop()
            stacks[target].append(c)
    print("".join([s[-1] for s in stacks]))

def f1(input):
    stacks, instructions = input
    for amount, source, target in instructions:
        cs = [stacks[source].pop() for i in range(amount)]
        cs.reverse()
        stacks[target].extend(cs)
    print("".join([s[-1] for s in stacks]))
