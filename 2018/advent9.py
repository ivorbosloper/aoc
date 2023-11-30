import enum
import re
from collections import deque


def parse(input):
    m = re.match(r"(\d+) players; last marble is worth (\d+) points", input)
    assert m
    return int(m.group(1)), int(m.group(2))


class Game:
    def __init__(self, nr_players) -> None:
        self.board = deque([0])
        self.current_index = 0
        self.scores = [0] * nr_players
        self.current_player = 0

    def add(self, marble: int):
        if marble % 23 == 0:
            remove_from = (self.current_index - 7 + len(self.board)) % len(self.board)
            remove_value = self.board[remove_from]
            self.board.remove(remove_value)
            self.scores[self.current_player] += marble + remove_value
            self.current_index = remove_from % len(self.board)
        else:
            place_at = (self.current_index + 1) % len(self.board) + 1
            self.board.insert(place_at, marble)
            self.current_index = place_at

        self.current_player = (self.current_player + 1) % len(self.scores)
        # elems = []
        # for index, marble in enumerate(self.board):
        #     elems.append(f"{marble: 2d}{'.' if index==self.current_index else ' '}")

        # print(f"[{self.current_player}] {''.join(elems)}")


def f1(input: list[int]):
    # print()
    players, high = input
    game = Game(players)
    for m in range(1, high + 1):
        game.add(m)
    return max(game.scores)


def f2(input: list[int]):
    return f1([input[0], input[1] * 100])
