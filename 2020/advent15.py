def parse(input):
    return [int(i) for i in input.split(",")]


def f1(input, end=2020):
    nrs = len(input)
    # start = input[::]
    last_map = {nr: i for i, nr in enumerate(input[:-1])}
    last = input[-1]
    # print(input, end="")
    for i in range(nrs, end):
        if last not in last_map:
            new_nr = 0
        else:
            new_nr = i-1 - last_map[last]
        last_map[last] = i-1
        last = new_nr
        # print(",", new_nr, end="")
    #print()
    return last


def f2(input):
    return f1(input, 30000000)
