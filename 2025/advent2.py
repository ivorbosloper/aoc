

def parse(line):
    return [tuple(a.split('-')) for a in line.split(',')]

def f1(ranges):
    invalids = []
    for r in ranges:
        start, end = r
        for i in range(int(start), int(end) + 1):
            s = str(i)
            if len(s) % 2: continue
            half = len(s) // 2
            if s[:half] == s[half:]:
                invalids.append(i)

    return sum(invalids)


def f2(ranges):
    invalids = []
    for r in ranges:
        start, end = r
        for i in range(int(start), int(end)+1):
            s = str(i)
            for ln in range(1, len(s) // 2+1):
                # test ln 1, ln 2, ln3
                if len(s) % ln: continue
                test = s[:ln] * (len(s) // ln)
                if test == s:
                    invalids.append(i)
                    break

    return sum(invalids)
