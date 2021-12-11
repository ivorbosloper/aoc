OUTCOMES = ["VALID", "INCOMPLETE", "CORRUPTED"]

OPEN = "([{<"
CLOSE = ")]}>"
VALUES = [3, 57, 1197, 25137]


def pars(line):
    queue = []
    for c in line:
        if c in OPEN:
            queue.append(c)
        else:
            if len(queue):
                last_open_tag = queue.pop()
                if OPEN.index(last_open_tag) == CLOSE.index(c):
                    continue
            return "CORRUPTED", c
    if len(queue):
        return "INCOMPLETE", "".join(CLOSE[OPEN.index(c)] for c in reversed(queue))
    return "VALID", ""


def f1(input):
    cnt = 0
    for line in input:
        reason, char = pars(line)
        # print(line, reason, char)
        if reason == "CORRUPTED":
            cnt += VALUES[CLOSE.index(char)]
    return cnt


def close_value(s):
    cnt = 0
    for c in s:
        cnt = cnt * 5 + (CLOSE.index(c)+1)
    return cnt


def f2(input):
    results = []
    for line in input:
        reason, data = pars(line)
        if reason == "INCOMPLETE":
            results.append(close_value(data))

    results.sort()
    return results[len(results)//2]
