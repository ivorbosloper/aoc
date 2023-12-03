import re
from dataclasses import dataclass

COLORS = ["red", "green", "blue"]


@dataclass
class Round:
    colors: list[int]

    def fits(self, mx: list[int]):
        return all(c <= mx for c, mx in zip(self.colors, mx))


@dataclass
class Game:
    game_nr: int
    rounds: list[Round]

    def fits(self, mx: list[int]):
        return all(round.fits(mx) for round in self.rounds)

    def max(self):
        return [max(c) for c in zip(*[s.colors for s in self.rounds])]


def parse_line(line):
    m = re.match(r"Game (\d+): (.*)", line)
    assert m
    game_nr, rest = int(m.group(1)), m.group(2)
    rounds: list[Round] = []
    for line2 in rest.split("; "):
        round = Round(colors=[0] * 3)
        rounds.append(round)
        for e in line2.split(", "):
            nr, color = e.split(" ")
            round.colors[COLORS.index(color)] = int(nr)
    return Game(game_nr=game_nr, rounds=rounds)


def f1(games: list[Game]):
    mx = [12, 13, 14]
    return sum(game.game_nr for game in games if game.fits(mx))


def f2(games: list[Game]):
    maxes = [game.max() for game in games]
    return sum(m[0] * m[1] * m[2] for m in maxes)
