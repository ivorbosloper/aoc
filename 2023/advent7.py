from operator import attrgetter
from typing import Counter

SIGNS = list(reversed("A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")))


class Card:
    def __init__(self, cards) -> None:
        self.cards = cards
        self.card_val = [SIGNS.index(c) for c in cards]
        counter = Counter(cards)
        group_count = Counter(v for v in counter.values() if v > 1)
        self.g_count = tuple([group_count[i] for i in range(5, 1, -1)])

    @property
    def value(self):
        return self.g_count, self.card_val


def calc(input, clz):
    suit: dict[Card, int] = {}
    for line in input:
        cards, val = line.split(" ")
        card, bid = clz(cards), int(val)
        suit[card] = bid

    cards = list(suit.keys())
    cards.sort(key=attrgetter("value"))

    return sum(index * suit[card] for index, card in enumerate(cards, start=1))


def f1(input):
    return calc(input, Card)


class Card2(Card):
    def __init__(self, cards) -> None:
        super().__init__(cards)
        if "J" not in cards:
            return
        for i, v in enumerate(cards):
            if v == "J":
                self.card_val[i] = -1
        counter = Counter(cards)
        jokers = counter.pop("J", 0)
        group_count = Counter(v for v in counter.values())
        if group_count:
            max_group = max(group_count)
            group_count[max_group] -= 1
        else:
            max_group = 0
        group_count[max_group + jokers] += 1
        self.g_count = tuple([group_count[i] for i in range(5, 1, -1)])


def f2(input):
    return calc(input, Card2)
