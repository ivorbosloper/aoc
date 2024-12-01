from io import StringIO

import pandas as pd


def parse(input):
    return pd.read_csv(StringIO(input), names=["1", "2"], sep=r'\s+')


def f1(input):
    l1 = input['1'].sort_values()
    l2 = input['2'].sort_values()
    return (abs(l1 - l2)).sum()


def f2(input):
    histogram = input['2'].value_counts()
    return int(sum(input['1'] * input['1'].map(histogram).fillna(0)))
