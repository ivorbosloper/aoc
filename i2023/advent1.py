import math


def parse(input):
    return [eval("(" + line + ")") for line in input.split("\n")]


def f1(input):
    return int(
        sum(
            max(math.sqrt(t[0] * t[0] + t[1] * t[1]) for t in tuples)
            for tuples in input
        )
    )


def f2(input):
    # pip install smallestenclosingcircle
    import smallestenclosingcircle

    return sum(smallestenclosingcircle.make_circle(tuples)[2] for tuples in input)
