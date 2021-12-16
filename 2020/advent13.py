import sys


def f1(input):
    ts = int(input[0])
    ids = [int(d) for d in input[1].split(',') if d.isdigit()]

    minutes, bus_id = sys.maxsize, 0
    for i in ids:
        s = i - (ts % i)
        if s < minutes:
            minutes = s
            bus_id = i
    return minutes * bus_id


def f2(input):
    ts = int(input[0])
    ids = [int(d) for d in input[1].split(',') if d.isdigit()]

    # t % 7 == 0, t % 13 == 1, t % 59 == 4, t%31 == 6, t % 19 ==
