from collections import defaultdict
import sys

parse_line = int


def calc(input, length):
    sum_count = defaultdict(int)
    for index, value in enumerate(input):
        if index >= length:
            if not sum_count[value]:
                return value
            # remove some sum_counts
            remove_index = index - length  # the sums of remove_index should be gone next round
            for value2 in input[remove_index + 1:index]:
                sum_count[input[remove_index] + value2] -= 1
        # add sum of previous
        for value2 in input[max(index-length, 0):index]:
            sum_count[value + value2] += 1
        # print(index, value, sum_count)
    raise Exception("fail")


def f1(input):
    return calc(input, 25)


def f2(input):
    nr = calc(input, 25)
    for index in range(len(input)):
        added, _min, _max = 0, sys.maxsize, -sys.maxsize
        for j in range(index, len(input)):
            value = input[j]
            added += value
            if value < _min:
                _min = value
            if value > _max:
                _max = value
            if added == nr:
                # print("minmax", _min, _max, input)
                return _min + _max
            if added > nr:
                break


def test():
    input = [int(i) for i in """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".split("\n")]
    # assert calc(input, 5) == 127

    assert calc(list(range(1, 26)) + [26, 1000], 25) == 1000  # 26 is valid
    assert calc(list(range(1, 26)) + [49, 1000], 25) == 1000  # 49 is valid
    assert calc(list(range(1, 26)) + [100], 25) == 100  # 100 is invalid
    assert calc(list(range(1, 26)) + [50], 25) == 50  # 50 is invalid

test()

