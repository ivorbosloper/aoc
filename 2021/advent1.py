#!/usr/bin/env python3
parse_line = int


def f1(lst):
    prev = 10000
    cnt = 0
    for i in lst:
        if i > prev:
            cnt += 1
        prev = i
    return cnt


def f2(lst):
    prev = []
    cnt = 0
    for i in lst:
        new = (prev[::] if len(prev) < 3 else prev[1:]) + [i]
        if len(prev) > 2 and len(new) > 2:
            if sum(new) > sum(prev):
                cnt += 1
        prev = new
    return cnt
