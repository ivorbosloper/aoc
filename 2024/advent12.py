from itertools import groupby
from operator import itemgetter

from util import BaseBoard, HV_VARIANTS
from collections import deque


class Board(BaseBoard[str]):
    def __init__(self, input):
        super().__init__(input)
        self.group = [[None for _x in range(self.width)] for _y in range(self.height)]
        self.group_count = []  # len == #groups, [1] == nr of elements per group

    def start_from(self, x, y):
        q = deque()
        group = len(self.group_count)
        count = 0
        q.append((x, y))
        while q:
            x, y = q.pop()
            if not self.group[y][x] is None:
                assert self.group[y][x] == group
                continue
            count += 1
            self.group[y][x] = group
            plant = self.board[y][x]
            for dx, dy in HV_VARIANTS:
                if self.get(x+dx, y+dy) == plant and self.group[y+dy][x+dx] is None:
                    q.append((x+dx, y+dy))
        self.group_count.append(count)

    def mark_groups(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.group[y][x] is not None:
                    continue
                self.start_from(x, y)

    def calc_fences(self):
        group_area = [0 for _ in self.group_count]
        for y, row in enumerate(self.board):
            for x, plant in enumerate(row):
                group = self.group[y][x]
                for dx, dy in HV_VARIANTS:
                    if self.get(x + dx, y + dy) != plant:
                        group_area[group] += self.group_count[group]
        return sum(group_area)

    """
    Fence points; we're going to mark the GRID points, on the corners of the cells
    
    AABB
    AABB
    
    Group A is going to have (0,0)-(1,0) and (1,0)-(2,0) on top. And then and (2,0)-(2,1) and (2,1)-(2,2) ...
    We'll add the parts as we detect an edge.
    
    Every grid-point is will be present twice, once as a start, and once as an end.
    We'll traverse all points in order, and see when we take a turn (when (dx, dy) changes)
    
    Hmmm, touching is a complex case, consider gridpoint (2,1). It's not present twice but 4 times.
    If there's more than one fence starting at a gridpoint, we'll stick to the line with the same 'origin'
    
    AA.
    A.A
    AAA
        
    """
    GRID_DELTAS = ((1, 0), (1, 1), (0, 1), (0, 0))

    def calc_fences2(self):
        result = 0
        def delta(p1, p2):
            return p2[0] - p1[0], p2[1] - p1[1]

        fence_lines = [[] for _ in self.group_count]  # from, to, origin
        for y, row in enumerate(self.board):
            for x, plant in enumerate(row):
                group = self.group[y][x]
                for hvi, hv in enumerate(HV_VARIANTS):
                    dx, dy = hv
                    if self.get(x + dx, y + dy) != plant:
                        gd1, gd2 = self.GRID_DELTAS[hvi], self.GRID_DELTAS[(hvi+1) % 4]
                        fence_lines[group].append(((x+gd1[0], y+gd1[1]), (x+gd2[0], y+gd2[1]), (x, y)))

        for group, lines in enumerate(fence_lines):
            fences = 0
            assert set(l[0] for l in lines) == set(l[1] for l in lines)
            from_to_origin = {k: [g[1:] for g in grp] for k, grp in groupby(sorted(lines), key=itemgetter(0))}

            while from_to_origin:
                prev, to_origins = next(iter(from_to_origin.items()))
                p, origin = to_origins[0]
                dlt = delta(prev, p)
                while p in from_to_origin:
                    to_origins = from_to_origin[p]
                    if len(to_origins) > 1:
                        # print(f"Handling squeeze point ({p})")
                        assert len(to_origins) == 2
                        to_origin = next(e for e in to_origins if e[1] == origin)
                        to, origin = to_origin
                        to_origins.remove(to_origin)
                    else:
                        to, origin = to_origins[0]
                        del from_to_origin[p]

                    to_delta = delta(p, to)
                    if to_delta != dlt:
                        fences += 1
                    # print(f"{group}: from {p} to {to} corner {to_delta != dlt}")
                    p = to
                    dlt = to_delta

            # print(group, self.group_count[group], fences)
            result += self.group_count[group] * fences
        return result


def parse(inp):
    return Board(inp.split("\n"))


def f1(board):
    board.mark_groups()
    return board.calc_fences()


def f2(board):
    board.mark_groups()
    return board.calc_fences2()
