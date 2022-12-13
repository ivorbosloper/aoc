import functools

def parse(input):
    return [
        [eval(p.strip()) for p in pairs.split('\n')] 
        for pairs in input.split("\n\n")
    ]

def compare(e1, e2):
    if isinstance(e1, int):
        if isinstance(e2, int):
            return e1 - e2
        else:
            return lst_compare([e1], e2)

    if isinstance(e2, int):
        return lst_compare(e1, [e2])
    return lst_compare(e1, e2)


def lst_compare(p1, p2):
    l1, l2 = len(p1), len(p2)
    index = 0
    while True:
        if index in (l1, l2):
            return l1 - l2  # longest list is king
        cmp = compare(p1[index], p2[index])
        if cmp != 0:
            return cmp
        index += 1
    return 0

def f1(pairs):
    total = 0
    for index, pair in enumerate(pairs):
        if lst_compare(*pair) <= 0:
            total += index + 1
    print(total)

def f2(pairs):
    lst = [e for l in pairs for e in l]  # flatten
    dividers = [ [[2]], [[6]] ]
    lst.extend(dividers)
    lst.sort(key=functools.cmp_to_key(compare))
    print((lst.index(dividers[0]) + 1) * (lst.index(dividers[1]) + 1))
