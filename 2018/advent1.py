def f1(input):
    return sum(map(int, input))


def f2(input):
    done = set()
    frq = 0
    while True:
        for line in input:
            if frq in done:
                return frq
            done.add(frq)
            frq += int(line)
