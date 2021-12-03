
def pseat(line):
    row = int(line[:-3].replace('B', '1').replace('F', '0'), 2)
    column = int(line[-3:].replace('R', '1').replace('L', '0'), 2)
    seat = row * 8 + column
    return row, column, seat


def f1(input):
    m = 0
    for line in input:
        row, column, seat = pseat(line)
        if seat > m:
            m = seat
    return m


def f2(input):
    lst = [pseat(line) for line in input]  # row, column, seat
    rows = sorted(set(r[0] for r in lst))
    by_seat = {r[2]: r for r in lst}
    start, end = min(by_seat), max(by_seat)

    for seat in range(start, end+1):
        if seat in by_seat:
            continue
        row = seat // 8
        if row in (rows[0], rows[-1]):
            continue
        if seat-1 in by_seat and seat+1 in by_seat:
            print(seat)
