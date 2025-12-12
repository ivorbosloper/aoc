from functools import reduce
import operator


OPERATORS =  {
    '+': operator.add,
    '*': operator.mul,
}

def parse(input):
    return input.split("\n")


def f1(input):
    input = [line.split() for line in input]
    result = 0
    for index in range(len(input[0])):
        col = [line[index] for line in input]
        result += reduce(OPERATORS[col[-1]], map(int, col[:-1]))
    return result


def f2(input):
    total = 0
    lst = []
    for x in range(len(input[0])-1, -1, -1):
        line = "".join([input[y][x] for y in range(len(input))])
        if not line.strip():
            assert lst == []
            continue
        lst.append(int(line[:-1].strip()))
        op = line[-1]
        if op != ' ':
            # print("adding", ", ".join([str(x) for x in lst]), reduce(OPERATORS[op], lst))
            total += reduce(OPERATORS[op], lst)
            lst = []
    assert lst == []
    return total
