from collections import deque
from typing import Deque

from util import BaseBoard

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
E, S, W, N = [0, 1, 2, 3]


class Board(BaseBoard):
    def fill(self, start=(0, 0, E)):
        board = self.board
        handled = [[0 for x in range(self.width)] for y in range(self.height)]
        q: Deque[tuple[int, int, int]] = deque([start])

        while q:
            x, y, dir_nr = q.pop()
            if not (0 <= x < self.width and 0 <= y < self.height):
                continue
            if handled[y][x] & 1 << dir_nr:
                continue

            handled[y][x] |= 1 << dir_nr
            current = board[y][x]
            compatible = "-" if DIRS[dir_nr][0] else "|"
            if current in (".", compatible):
                pass
            elif current in "|-":
                dir_nr = (dir_nr + 1) % 4
                q.append((x + DIRS[dir_nr][0], y + DIRS[dir_nr][1], dir_nr))
                dir_nr = (dir_nr + 2) % 4
            elif current == "\\":
                dir_nr = [1, 0, 3, 2][dir_nr]
            elif current == "/":
                # E->N, S->W, W->S, N->E
                dir_nr = 3 - dir_nr
            else:
                raise Exception(f"Found {current} on {x},{y}")
            q.append((x + DIRS[dir_nr][0], y + DIRS[dir_nr][1], dir_nr))

        return sum(
            handled[y][x] > 0 for x in range(self.width) for y in range(self.height)
        )

    def edge_entries(self):
        # E, S, W, N
        for y in range(self.height):
            yield 0, y, 0
            yield self.width - 1, y, 2
        for x in range(self.width):
            yield x, 0, 1
            yield x, self.height - 1, 3


def f1(input):
    board = Board(input)
    return board.fill()


def f2(input):
    board = Board(input)
    return max(board.fill(s) for s in board.edge_entries())
