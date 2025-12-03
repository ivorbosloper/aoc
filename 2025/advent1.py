

def parse_line(line):
    return (1 if line[0] == 'R' else -1), int(line[1:])


def f1(tuples):
    count = 0
    dial = 50
    for direction, nr in tuples:
        dial = (100 + dial + (direction * nr)) % 100
        count += dial == 0
    return count

def f2(tuples):
    count = 0
    dial = 50
    for direction, nr in tuples:
        assert 0 <= dial < 100
        is_zero = dial == 0
        dial += (direction * nr)
        if 0 < dial < 100:
            continue
        if dial == 0:
            count += 1
        elif dial < 0:
            count += (not is_zero) + (-dial)//100
        else:
            count += dial//100
        dial %= 100
    return count
