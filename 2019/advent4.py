def matches(i):
    double = False
    previous = None
    for _ in range(6):
        d = i % 10
        i //= 10
        if previous is None:
            pass
        elif d == previous:
            double = True
        elif previous < d:
            return False
        previous = d

    return double


def f1(input):
    assert all(matches(i) for i in [122345, 111123, 111111])
    assert all(not matches(i) for i in [223450, 123789])

    start, end = map(int, input[0].split("-"))
    return sum(matches(i) for i in range(start, end + 1))


def matches2(i):
    match_count = 0
    double = None
    previous = None
    for _ in range(6):
        d = i % 10
        i //= 10
        if previous is None:
            pass
        elif d == previous:
            if not match_count:
                match_count = 2
            else:
                match_count += 1
        elif previous < d:
            return False
        if d != previous and match_count:
            if match_count == 2:
                double = True
            match_count = 0
        previous = d

    return double or match_count == 2


def f2(input):
    assert all(matches(i) for i in [122345, 111123, 111111])
    assert all(not matches(i) for i in [223450, 123789])

    start, end = map(int, input[0].split("-"))
    return sum(matches2(i) for i in range(start, end + 1))
