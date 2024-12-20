from collections import deque, defaultdict

from util import BaseBoard, HV_VARIANTS


class Board(BaseBoard):
    def __init__(self, input):
        super().__init__(input)
        self.fastest = [[None for _x in range(self.width)] for _y in range(self.height)]
        for y, line in enumerate(input):
            for char in 'SE':
                if char in line:
                    x = line.index(char)
                    self.board[y][x] = '.'
                    if char == 'S':
                        self.start = (x, y)
                    else:
                        self.end = (x, y)

    def search(self):
        x, y = self.start
        q = deque([self.start])
        self.fastest[y][x] = 0
        while q:
            x, y = q.popleft()
            # print(x, y)
            current = self.fastest[y][x]
            assert current is not None
            for dx, dy in HV_VARIANTS:
                nx, ny = x + dx, y + dy
                if self.get(nx, ny) != ".":
                    continue
                if self.fastest[ny][nx] is None:
                    self.fastest[ny][nx] = current + 1
                    q.append((nx, ny))
                else:
                    assert current + 1 >= self.fastest[ny][nx]
        return self.fastest[self.end[1]][self.end[0]]

    def cheats(self):
        limit = 100 if self.width > 20 else 1
        save_count = defaultdict(int)
        for y, row in enumerate(self.board):
            for x, e in enumerate(row):
                current = self.fastest[y][x]
                if current is None: # unreachable
                    continue
                for dx, dy in HV_VARIANTS:
                    if self.get(x + dx, y + dy) == "#" and self.get(x + dx*2, y + dy*2) == ".":
                        jump_to = self.fastest[y + dy*2][x + dx*2]
                        if jump_to is not None and current+2 < jump_to:
                            save = jump_to - (current+2)
                            assert save > 0
                            save_count[save] += 1

        # for save, count in save_count.items():
        #     print(f"There are {count} cheats that save {save} picoseconds.")
        return sum(count for save, count in save_count.items() if save >= limit)

    def cheats2(self):
        limit = 100 if self.width > 20 else 50
        save_count = defaultdict(int)
        for y, row in enumerate(self.board):
            for x, e in enumerate(row):
                origin = self.fastest[y][x]
                if origin is None: # unreachable
                    continue
                # Now, start a new shortest-path breadth-first search (max 20 steps)
                # print(f"Fix ({x}, {y})")
                q = deque([(x, y)])
                fastest = {(x, y): 0}  # (x, y) -> fastest
                while q:
                    _x, _y = p = q.popleft()
                    assert (current := fastest[p]) <= 20
                    block = self.board[_y][_x]
                    if block == ".":
                        # could land here
                        jump_to = self.fastest[_y][_x]
                        if jump_to is not None and origin + current < jump_to:
                            save = jump_to - (origin + current)
                            assert save > 0
                            save_count[save] += 1

                    for dx, dy in HV_VARIANTS:
                        nx, ny = _x + dx, _y + dy
                        block = self.get(nx, ny)
                        if block is None:
                            continue  # outside board
                        if (nx, ny) in fastest:
                            continue  # already visited this in breadth-first search
                        if current < 20:
                            fastest[(nx, ny)] = current + 1
                            q.append((nx, ny))

        # for save, count in save_count.items():
        #     if save >= 50:
        #         print(f"There are {count} cheats that save {save} picoseconds.")
        return sum(count for save, count in save_count.items() if save >= limit)


def parse(inp):
    return Board(inp.split("\n"))


def f1(board):
    board.search()
    return board.cheats()

def f2(board):
    board.search()
    return board.cheats2()

