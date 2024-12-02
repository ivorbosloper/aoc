import pandas as pd
# Conclusion of the day; Learned a lot, pandas is not simpler for simple problems


def parse(input):
    return [[int(a) for a in line.split()] for line in input.split("\n")]


def is_ok(line):
    diff = [b-a for a, b in zip(line[:-1], line[1:])]
    up_or_down = all(e > 0 for e in diff) or all(e < 0 for e in diff)
    return up_or_down and max(abs(e) for e in diff) <= 3


def f1(input):
    return sum(is_ok(line) for line in input)


def f1_pd(input):
    input = pd.DataFrame(input)
    difference = input.diff(axis=1).truncate(before=1, axis=1).ffill(axis="columns")
    up_or_down = (difference > 0).all(axis="columns") | (difference < 0).all(axis="columns")
    ok = up_or_down & (difference.abs().max(axis="columns") <= 3)
    return ok.sum()


def f2(input):
    def is_ok_any(line):
        return any(is_ok(line[:i] + line[i+1:]) for i in range(len(line)))

    return sum(is_ok_any(line) for line in input)


def f2_pd(input):
    base = pd.DataFrame(input)

    ok = pd.Series([False] * base.shape[0], dtype=bool)
    for i in range(base.shape[1]):
        df = base[base.columns.difference([i])]
        difference = df.diff(axis=1).truncate(before=1, axis=1)
        up_or_down = (difference.isna() | (difference > 0)).all(axis="columns") | (difference.isna() | (difference < 0)).all(axis="columns")
        ok |= up_or_down & (difference.fillna(0).abs().max(axis="columns") <= 3)
    return ok.sum()
