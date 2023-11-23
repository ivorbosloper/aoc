from collections import Counter


def f1(input):
    c = Counter(j for i in input for j in set(Counter(i).values()))
    return c[2] * c[3]


def f2(input):
    def similarity(s):
        return sum(c1 == c2 for c1, c2 in zip(*s))

    pair = max(
        ((s1, s2) for i, s1 in enumerate(input) for s2 in input[i + 1 :]),
        key=similarity,
    )
    return "".join([c1 for c1, c2 in zip(*pair) if c1 == c2])
