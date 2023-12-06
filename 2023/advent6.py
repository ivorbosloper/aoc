import math
import re


def naive(t, dist):
    counter = 0
    for hold in range(1, t):
        d = hold * (t - hold)
        if d > dist:
            counter += 1
    return counter


def f1(input):
    ls = [[int(a) for a in re.findall(r"\d+", line)] for line in input]
    ts = tuple(zip(*ls))
    result = 1
    for t, dist in ts:
        counter = naive(t, dist)
        if counter > 0:
            result *= counter
    return result


def abc(a, b, c):
    sqr = math.sqrt(b * b - 4 * a * c)
    return (-b + sqr) / 2 * a, (-b - sqr) / 2 * a


def efficient(t, dist):
    t1, t2 = abc(-1, t, -dist)
    return int(t2) - int(t1)


def f2(input):
    ls = [int("".join(re.findall(r"\d+", line))) for line in input]
    t, dist = ls
    # y = x * (t-x)
    # 0 = -x^2 + tx - dist
    # ABC formula
    # ABC = -1, time, -dist

    # x = -b +- sqrt(b^2 - 4ac)
    # x = -t + sqrt(t^2 + 4dist)
    return efficient(t, dist)
