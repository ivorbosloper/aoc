from collections import defaultdict
from email.policy import default
from queue import PriorityQueue

from util import BaseBoard

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
E, S, W, N = [0, 1, 2, 3]
INFINITY = 1000000

Pos = tuple[int, int]  # x, y
MoveState = tuple[int, int]  # direction, steps
Item = tuple[int, Pos, MoveState]  # steps, (x, y), (direction, steps)


class Board(BaseBoard[int]):
    func = int

    def allowed_next_steps(self, current_direction, steps):
        for d in range(4):
            if steps > 0:  # only check after start
                if d == (current_direction + 2) % 4:
                    continue  # no reverse
                if steps == 3 and current_direction == d:
                    continue  # not more then 3 steps
            yield d

    def travel(self):
        start: Pos = (0, 0)
        end: Pos = self.width - 1, self.height - 1

        # for each pos, lowest total steps per movestate
        visited: dict[Pos, dict[MoveState, int]] = defaultdict(
            lambda: defaultdict(lambda: INFINITY)
        )
        q = PriorityQueue[Item]()
        q.put((0, start, (0, 0)))
        while not q.empty():
            total_steps, pos, move_state = q.get()
            if pos == end:  # finish
                return total_steps
            x, y = pos
            direction, steps = move_state
            if visited[pos][move_state] <= total_steps:
                continue  # been here before in same dir+steps with fewer total_steps
            visited[pos][move_state] = total_steps

            for d in self.allowed_next_steps(direction, steps):
                nx, ny = x + DIRS[d][0], y + DIRS[d][1]
                value_nx_ny = self.get(nx, ny)
                if value_nx_ny is None:
                    continue  # nx, ny outside board
                q.put(
                    (
                        total_steps + value_nx_ny,
                        (nx, ny),
                        (d, (steps + 1 if d == direction else 1)),
                    )
                )

        raise Exception("Failed to find solution")


def f1(input):
    board = Board(input)
    return board.travel()


class Board2(Board):
    def allowed_next_steps(self, current_direction, steps):
        for d in range(4):
            if steps > 0:  # only check after start
                if d == (current_direction + 2) % 4:
                    continue  # no reverse
                if steps < 4 and current_direction != d:
                    continue  # not less then 4 steps in same direction
                if steps >= 10 and current_direction == d:
                    continue  # not more then 4 steps in same direction
            yield d


def f2(input):
    board = Board2(input)
    return board.travel()
