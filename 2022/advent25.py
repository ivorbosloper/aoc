pwr = [5**i for i in range(15)]
signs = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}
to_sign = {v: k for k, v in signs.items()}

def to_int(s):
    result = 0
    for c in s:
        result = result * 5 + signs[c]
    # assert to_snafu(result) == s, f"{result}: {to_snafu(result)} != {s}"
    return result


def to_snafu(i):
    s = []
    while i>0:
        r = i % 5
        i //= 5
        if r > 2:
            r -= 5
            i += 1
        s.append(to_sign[r])
    return "".join(reversed(s))


parse_line = to_int

def f1(input):
    input_sum = sum(input)
    return to_snafu(input_sum)
