
def parse(input):
    a, b = input.split("\n\n")
    ranges = [tuple(map(int, line.split("-"))) for line in a.split("\n")]
    nrs = [int(line) for line in b.split("\n")]
    return ranges, nrs

def f1(input):
    ranges, nrs = input
    is_ok = []
    for nr in nrs:
        for start, end in ranges:
            if start <= nr <= end:
                is_ok.append(nr)
                break
    return len(is_ok)

def f2(input):
    ranges, nrs = input
    ranges = sorted(ranges)

    result = []
    i = 0
    length = len(ranges)
    while i < length:
        start, end = ranges[i]
        i+=1
        while i < length and ranges[i][0] <= end:
            end = max(end, ranges[i][1])
            i += 1
        result.append((start, end))
    print (result)
    # not 336044116701033
    return sum(r[1] - r[0]+1 for r in result)

