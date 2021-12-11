from collections import defaultdict


def f1(input):
    count = 0
    for line in input:
        before, after = line.split(" | ")
        frequency = defaultdict(int)
        for segment in after.split(" "):
            frequency[len(segment)] += 1
        count += sum(frequency[i] for i in (2, 3, 4, 7))
    return count


nrs = ["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]


def str_sort(s):
    return "".join(sorted(c for c in s))


def f2(input):
    count = 0
    for line in input:
        before, after = line.split(" | ")
        # freqs = [8, 6, 8, 7, 4, 9, 7]  # freq(a) == 8, freq(b) == 6
        # possible_bit = {chr(ord('a') + wire): set(range(8)) for wire in range(8)}
        # [1, 7, 4, len(5+5+5), len(6+6+6), 8]
        segments = list(sorted([str_sort(s) for s in before.split(" ")], key=len))
        sets = [set(s) for s in segments]
        numbers = [1, 7, 4, None, None, None, None, None, None, 8]

        pin_a = next(c for c in segments[1] if c not in segments[0])
        index_nr_6 = next(i for i in range(6, 9) if not sets[i].issuperset(sets[0]))  # nr 6 is missing pins from nr 1
        numbers[index_nr_6] = 6
        pin_c = next(c for c in segments[9] if c not in segments[index_nr_6])
        pin_f = next(c for c in segments[0] if c != pin_c)

        index_nr_3 = next(i for i in range(3, 6) if sets[i].issuperset(sets[1]))
        index_nr_2 = next(i for i in range(3, 6) if i != index_nr_3 and pin_f not in segments[i])
        index_nr_5 = next(i for i in range(3, 6) if i not in (index_nr_3, index_nr_2))

        numbers[index_nr_3] = 3
        numbers[index_nr_2] = 2
        numbers[index_nr_5] = 5

        pin_e = next(c for c in segments[9] if c not in segments[index_nr_5] and c != pin_c)
        index_nr_9 = next(i for i in range(6, 9) if i != index_nr_6 and pin_e not in segments[i])
        index_nr_0 = next(i for i in range(6, 9) if i not in (index_nr_6, index_nr_9))
        numbers[index_nr_9] = 9
        numbers[index_nr_0] = 0

        sorted_string_to_number = {segments[i]: str(numbers[i]) for i in range(10)}
        nr = int("".join([sorted_string_to_number[str_sort(s)] for s in after.split(" ")]))
        count += nr
    return count


def f2(input):
    count = 0
    for line in input:
        before, after = line.split(" | ")
        # freqs = [8, 6, 8, 7, 4, 9, 7]  # freq(a) == 8, freq(b) == 6
        # [e, b, None, None, None, None, f]


        # [1, 7, 4, len(5+5+5), len(6+6+6), 8]
        segments = list(sorted([str_sort(s) for s in before.split(" ")], key=len))
        sets = [set(s) for s in segments]
        numbers = [1, 7, 4, None, None, None, None, None, None, 8]
