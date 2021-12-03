def parse(input):
    result, tmp = [], []
    for line in input.split('\n'):
        if line:
            tmp.append(line)
        elif tmp:
            result.append(tmp)
            tmp = []
    if tmp:
        result.append(tmp)
    return result


def print_f(input, func):
    return sum(len(func(group)) for group in input)


def f1(input):
    print_f(input, lambda group: set(c for line in group for c in line))


def f2(input):
    def f(group):
        s = set(group[0])
        for g in group[1:]:
            s = s & set(g)
        return s
    print_f(input, f)
