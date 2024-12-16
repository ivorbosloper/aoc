from queue import PriorityQueue

from util import BaseBoard, HV_VARIANTS


class Board(BaseBoard):
    def __init__(self, inp):
        super(Board, self).__init__(inp)
        self.start = self.find("S")
        # self.board[self.start[1]][self.start[0]] = "."

    def fastest(self):
        cheapest = {}  # lowest cost to reach (x, y, direction)
        q = PriorityQueue()
        q.put((0, (self.start[0], self.start[1], 0)))
        while not q.empty():
            cost, posdir = q.get()
            if posdir in cheapest and cheapest[posdir] <= cost:
                continue
            cheapest[posdir] = cost
            x, y, direction = posdir
            if self.board[y][x] == "E":
                return cheapest, cost
            assert self.board[y][x] in "S."
            dx, dy = HV_VARIANTS[direction]
            nxt = self.board[y+dy][x+dx]
            if nxt in ".E":
                q.put((cost + 1, (x+dx, y+dy, direction)))
            else:
                assert nxt in "S#", nxt

            q.put((cost + 1000, (x, y, (direction-1) % 4)))
            q.put((cost + 1000, (x, y, (direction+1) % 4)))
        raise StopIteration("No exit found")

    def reverse_match_cheapest(self, cheapest):
        # cheapest: (x, y, direction) -> lowest cost to reach cost to reach position + direction
        q = PriorityQueue()
        end = self.find("E")
        options = [cheapest.get((end[0], end[1], direction)) for direction in range(4)]
        cost = next(e for e in options if e is not None)

        reached = set()
        for direction in range(4):
            q.put((cost, (end[0], end[1], direction)))

        while not q.empty():
            cost, posdir = q.get()
            x, y, direction = posdir
            reached.add((x, y))
            assert self.board[y][x] != "#"

            # try step in reverse direction
            dx, dy = HV_VARIANTS[direction]
            tpl = (x-dx, y-dy, direction)
            if cheapest.get(tpl) == cost - 1:
                q.put((cost - 1, tpl))

            # try turning back
            for turn in (-1, 1):
                tpl = x, y, (direction + turn) % 4
                if cheapest.get(tpl) == cost - 1000:
                    q.put((cost - 1000, tpl))

        return len(reached)


def parse(inp):
    return Board(inp.split("\n"))


def f1(inp):
    cheapest, cost = inp.fastest()
    return cost


def f2(inp):
    cheapest, cost = inp.fastest()
    return inp.reverse_match_cheapest(cheapest)
