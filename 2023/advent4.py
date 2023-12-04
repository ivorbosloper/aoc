import re
from collections import defaultdict


def nrs(s):
    return [int(a) for a in re.findall(r"\d+", s)]


def parse_line(line):
    m = re.match(r"Card\s+(\d+):\s+(.*)\s+\|\s+(.*)", line)
    card_nr = int(m.group(1))
    return card_nr, nrs(m.group(2)), nrs(m.group(3))


def f1(input):
    def value(n: int) -> int:
        return pow(2, n - 1) if n > 0 else 0

    return sum(
        value(len(set(winning).intersection(set(my_nrs))))
        for card_nr, winning, my_nrs in input
    )


def f2(input):
    cards = {card_nr: 1 for card_nr, _a, _b in input}
    for card_nr, winning, my_nrs in input:
        overlaps = len(set(winning).intersection(set(my_nrs)))
        factor = cards[card_nr]
        for i in range(overlaps):
            cards[card_nr + 1 + i] += factor
    return sum(cards.values())
