from util import HV_VARIANTS, BaseBoard
from collections import deque

def hval(c):
    if c == 'S':
        return 0
    if c == 'E':
        return 25
    return ord(c) - ord('a')

class Board(BaseBoard):
    def __init__(self, input):
        super().__init__(input, hval)
        self.start = self.end = None
        for y, row in enumerate(input):
            for x, c in enumerate(row):
                if c == 'S':
                    self.start = x, y
                elif c == 'E':
                    self.end = x, y
        assert self.start and self.end

    def sim(self):
        dist = [[0 if (x, y) == self.start else None for x in range(self.width)] for y in range(self.height)]
        queue = deque()
        queue.append(self.start)
        while len(queue):
            x, y = queue.popleft()
            so_far = dist[y][x]
            for dx, dy in HV_VARIANTS:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.width and 0 <= ny < self.height \
                        and dist[ny][nx] is None \
                        and self.board[ny][nx] - self.board[y][x] <= 1:
                    dist[ny][nx] = so_far + 1
                    queue.append((nx, ny))
        print(dist[self.end[1]][self.end[0]])

    def sim2(self):
        dist = [[0 if (x, y) == self.end else None for x in range(self.width)] for y in range(self.height)]
        queue = deque()
        queue.append(self.end)
        while len(queue):
            x, y = queue.popleft()
            so_far = dist[y][x]
            for dx, dy in HV_VARIANTS:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.width and 0 <= ny < self.height \
                        and dist[ny][nx] is None \
                        and self.board[y][x] - self.board[ny][nx] <= 1:
                    dist[ny][nx] = so_far + 1
                    if self.board[ny][nx] == 0: # reached it!
                        print(so_far + 1)
                        return
                    queue.append((nx, ny))
        raise Exception("Failed")

def f1(input):
    Board(input).sim()

def f2(input):
    Board(input).sim2()
