def calc(lst):
    count = [0] * len(lst[0])
    for line in lst:
        for i, c in enumerate(line):
            if c == '1':
                count[i] += 1
    return count


def get_masks(lst):
    count = calc(lst)
    avg = len(lst) / 2
    return "".join(["1" if v >= avg else "0" for v in count]),\
        "".join(["1" if v < avg else "0" for v in count])


def f1(input):
    lst = [i for i in input]
    gamma, eps = get_masks(lst)
    return int(gamma, 2) * int(eps, 2)


def most_common_bit(vals, index):
    return "1" if len([v for v in vals if v[index] == '1']) >= len(vals) / 2 else "0"


def f2(input):
    lst = [i for i in input]
    vals1, vals2 = set(lst), set(lst)
    answer1, answer2 = None, None
    for index in range(len(lst[0])):
        bit = most_common_bit(vals1, index)
        for v in list(vals1):
            if v[index] != bit:
                vals1.remove(v)

        bit = most_common_bit(vals2, index)
        for v in list(vals2):
            if v[index] == bit:
                vals2.remove(v)

        if len(vals1) == 1: answer1 = next(iter(vals1))
        if len(vals2) == 1: answer2 = next(iter(vals2))

    return int(answer1, 2) * int(answer2, 2)
