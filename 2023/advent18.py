import re
from collections import deque

from util import BaseBoard

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
MAP = dict(zip("RDLU", DIRS))
Pos = tuple[int, int]


def parse_line(line):
    assert (m := re.match(r"([RUDL]) (\d+) \(#(\w+)\)", line))
    d, nr, color = m.groups()
    return d, int(nr), color


class Board(BaseBoard[str]):
    def __init__(self, input):
        bbox = [0, 0, 0, 0]  # min_x, min_y, max_x, max_y
        x, y = 0, 0
        for d, nr, color in input:
            x += MAP[d][0] * nr
            y += MAP[d][1] * nr
            if x < bbox[0]:
                bbox[0] = x
            if x > bbox[2]:
                bbox[2] = x
            if y < bbox[1]:
                bbox[1] = y
            if y > bbox[3]:
                bbox[3] = y
        self.bbox = tuple(bbox)
        width, height = bbox[2] - bbox[0] + 1, bbox[3] - bbox[1] + 1
        super().__init__(["." * width for _ in range(height)])
        assert self.width == bbox[2] - bbox[0] + 1
        assert self.height == bbox[3] - bbox[1] + 1
        board = self.board
        x, y = -bbox[0], -bbox[1]
        # board[y][x] = color
        for d, nr, color in input:
            for i in range(nr):
                x += MAP[d][0]
                y += MAP[d][1]
                board[y][x] = "#"

    def outside_black(self):
        q = deque[Pos]()
        for x in range(self.width):
            q.append((x, 0))
            q.append((x, self.height - 1))
        for y in range(self.height):
            q.append((0, y))
            q.append((self.width - 1, y))
        while q:
            x, y = q.pop()
            color = self.get(x, y)
            if color != ".":
                continue
            self.board[y][x] = " "
            for dx, dy in DIRS:
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    q.append((x + dx, y + dy))


def f1(input):
    board = Board(input)
    board.outside_black()
    return sum(
        board.board[y][x] != " "
        for x in range(board.width)
        for y in range(board.height)
    )
