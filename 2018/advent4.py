import itertools
import operator
from collections import defaultdict
from datetime import date, timedelta

try:
    from itertools import batched  # type: ignore
except ImportError:
    from itertools import islice

    def batched(iterable, n):
        # batched('ABCDEFG', 3) --> ABC DEF G
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield batch


class Day:
    def __init__(self, dt, guard) -> None:
        self.dt = dt
        self.guard = guard
        self.intervals = []

    @property
    def is_empty(self):
        return len(self.intervals) == 0

    @property
    def is_sleeping(self):
        return 1 == len(self.intervals) % 2

    def add(self, tm, wake_up: bool):
        if self.is_empty and wake_up:
            return
        assert wake_up == self.is_sleeping
        assert self.is_empty or self.intervals[-1] <= tm
        self.intervals.append(tm)

    def finish(self):
        assert self.dt is not None
        if self.is_sleeping:
            self.intervals.append(60)
        return self


def parse(input):
    input = sorted(input.split("\n"))
    result = []

    day = None
    for line in input:
        dt, tm, sentence = line[1:11], line[12:17], line[19:]
        _type = sentence[:5]
        assert _type in ("Guard", "falls", "wakes")
        if tm.startswith("23:"):
            tm = 0
            dt = (date.fromisoformat(dt) + timedelta(days=1)).isoformat()
        else:
            tm = int(tm[3:])

        if day and day.dt != dt:
            result.append(day.finish())
            day = None
        if day is None:
            assert _type == "Guard"
            day = Day(dt, int(sentence[7:15].split(" ")[0]))
        day.add(tm, _type != "falls")
    if day:
        result.append(day.finish())

    return result


def calc_histogram(days):
    histogram = [0] * 60
    for day in days:
        for x, y in batched(day.intervals, 2):
            for i in range(x, y):
                histogram[i] += 1
    return histogram


def f1(input):
    total_sleep = defaultdict(int)
    for day in input:
        total_sleep[day.guard] += sum(y - x for x, y in batched(day.intervals, 2))
    guard, count = max((g for g in total_sleep.items()), key=operator.itemgetter(1))

    histogram = calc_histogram([day for day in input if day.guard == guard])
    minute = max(enumerate(histogram), key=operator.itemgetter(1))[0]
    return guard * minute


def f2(input):
    key = operator.attrgetter("guard")
    input_sorted = sorted(input, key=key)
    mx = (0, 0, 0)  # guard, minute, count

    for guard, days in itertools.groupby(input_sorted, key=key):
        histogram = calc_histogram(days)
        for minute, count in enumerate(histogram):
            if count > mx[2]:
                mx = (guard, minute, count)

    return mx[0] * mx[1]
