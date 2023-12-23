from collections import defaultdict, deque
from distutils import ccompiler
from typing import Deque

from util import BaseBoard

Path = tuple[int, ...]
Item = tuple[Path, int]


class Board(BaseBoard):
    def nr(self, x: int, y: int):
        return y * self.width + x

    def pos(self, i: int):
        return i % self.width, i // self.width

    def longest_route(self, f1=True):
        change = (-1, 1, -self.width, self.width)
        cchange = tuple("." + x for x in "<>^v") if f1 else ("<>^v.",) * 4
        routes_done: dict[int, set[Path]] = defaultdict(set)
        board = sum(self.board, [])
        start = 1
        end = self.width * self.height - 2

        q: Deque[Item] = deque()
        q.append((tuple(), start))
        while q:
            done, p = q.popleft()
            sorted_done = tuple(sorted(done))
            if sorted_done in routes_done[p]:
                # we started at this part with exactly same history positions
                continue
            routes_done[p].add(sorted_done)
            done += (p,)
            for d in range(4):
                tp = p + change[d]
                if tp in done:
                    continue  # not second time same block
                if not (0 <= tp <= end and board[tp] in cchange[d]):
                    # should be inside board, and allowable square
                    continue
                q.append((done, tp))
        return max(len(s) for s in routes_done[end])

    def longest_route2(self):
        # more efficient
        change = (-1, 1, -self.width, self.width)
        board = sum(self.board, [])
        mx = [0 for _ in board]
        end = self.width * self.height - 2

        dirs = [-1 for _ in board]
        path = [0 for _ in board]
        path[0] = 1
        index = 0
        while index >= 0:
            if dirs[index] >= 3:
                index -= 1
                continue
            dirs[index] += 1
            tp = path[index] + change[dirs[index]]
            if not (0 <= tp <= end):
                continue
            try:
                if board[tp] == "#" or path.index(tp, 0, index) >= 0:
                    continue
            except ValueError:
                pass
            index += 1
            if mx[tp] < index:
                mx[tp] = index
            path[index] = tp
            dirs[index] = -1

        return mx[end]

    def longest_route3(self):
        change = (-1, 1, -self.width, self.width)
        board = sum(self.board, [])
        end = self.width * self.height - 2

        # Node --> [(Node, distance)]
        graph: dict[int, list[tuple[int, int]]] = {
            i: [(i + d, 1) for d in change if 0 <= i + d <= end and board[i + d] != "#"]
            for i, c in enumerate(board)
            if c != "#"
        }

        def shortcut(start: int, stop: int):
            d = 1
            while len(es := graph[stop]) == 2:
                index = es[0][0] == start
                start, stop, d = stop, es[index][0], d + es[index][1]
            return stop, d

        # for i, edges in graph.items():
        #     graph[i] = [shorten(i, n) for n, d in edges]
        graph = {i: [shortcut(i, n) for n, d in edges] for i, edges in graph.items()}
        handled = set()

        def distance(node, dist, best):
            if node == end:
                return dist
            if node in handled:
                return best

            handled.add(node)
            try:
                return max(distance(n, d + dist, best) for n, d in graph[node])
            finally:
                handled.discard(node)

        print(distance(1, 0, 0))


def f1(input):
    board = Board(input)
    return board.longest_route()


def f2(input):
    board = Board(input)
    return board.longest_route3()
