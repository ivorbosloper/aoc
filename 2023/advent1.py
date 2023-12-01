import re


def p(a):
    digits = [b for b in a if b.isdecimal()]
    return int(digits[0] + digits[-1])


def f1(input):
    return 0  # sum(p(a) for a in input)


nrs = "one,two,three,four,five,six,seven,eight,nine"
mapping = dict(zip(nrs.split(","), map(str, range(1, 10))))
regex = re.compile("(" + nrs.replace(",", "|") + ")")


def convert(a):
    return mapping.get(a, a)


def f2(input):
    match_string = "(" + nrs.replace(",", "|") + "|" + "|".join(mapping.values()) + ")"
    print(match_string)
    first = re.compile(match_string)
    last = re.compile(".*" + match_string)

    result = 0
    for line in input:
        m1 = convert(first.search(line).group(1))
        m2 = convert(last.search(line).group(1))
        result += int(m1 + m2)

    return result
    # return sum(p(convert(a)) for a in input)
    # too high 55725
