from collections import defaultdict
from queue import PriorityQueue

from util import BaseBoard

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))

Pos = tuple[int, int]  # x, y
MoveState = tuple[int, int]  # direction, steps
QItem = tuple[int, Pos, MoveState]  # steps, (x, y), (direction, steps)


class Board(BaseBoard[int]):
    func = int

    def allowed_next_steps(self, current_direction, steps):
        for d in range(4):
            if d == (current_direction + 2) % 4:
                continue  # no reverse
            if steps == 3 and current_direction == d:
                continue  # not more then 3 steps in same direction
            yield d

    def travel(self):
        start: Pos = (0, 0)
        end: Pos = self.width - 1, self.height - 1

        # for each pos, lowest total steps per movestate
        visited: dict[Pos, dict[MoveState, int]] = defaultdict(dict)
        q = PriorityQueue[QItem]()
        q.put((0, start, (0, 0)))
        while not q.empty():
            total_steps, pos, move_state = q.get()
            if pos == end:  # finish
                return total_steps
            direction, steps = move_state
            if visited[pos].get(move_state, 1000000) <= total_steps:
                continue  # been here before in same dir+steps with fewer total_steps
            visited[pos][move_state] = total_steps

            for d in self.allowed_next_steps(direction, steps):
                nx, ny = pos[0] + DIRS[d][0], pos[1] + DIRS[d][1]
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
    return Board(input).travel()


class Board2(Board):
    def allowed_next_steps(self, current_direction, steps):
        for d in range(4):
            if d == (current_direction + 2) % 4:
                continue  # no reverse
            if 0 < steps < 4 and current_direction != d:
                continue  # not less then 4 steps in same direction
            if steps >= 10 and current_direction == d:
                continue  # not more then 10 steps in same direction
            yield d


def f2(input):
    return Board2(input).travel()
