from util import BaseBoard, HV_VARIANTS
import re
DIRS = ">v<^"


class Board(BaseBoard[str]):
    def __init__(self, input, func=None):
        super().__init__(input)
        for y, line in enumerate(input):
            if m := re.search(r"[>v<^]", line):
                # x, y, direction
                self.guard = m.start(), y, DIRS.index(m.group())
                break
        self.board[self.guard[1]][self.guard[0]] = "."

    def step(self):
        x, y, direction = self.guard
        dx, dy = HV_VARIANTS[direction]

        new_x, new_y = x + dx, y + dy
        step_into = self.get(new_x, new_y)
        if step_into is None:
            return   # of the board
        elif step_into == '#':
            self.guard = x, y, (direction + 1) % 4
        else:
            self.guard = new_x, new_y, direction
        return self.guard

    def __str__(self):
        x, y, direction = self.guard
        return "\n".join("".join(DIRS[direction] if i == x and j == y else e
                                 for i, e in enumerate(row)) for j, row in enumerate(self.board))

    def take_steps(self):
        done = {self.guard}
        while new := self.step():
            if new in done:
                raise StopIteration("Loop detected")
            done.add(new)
        return done

    def has_loop(self):
        try:
            self.take_steps()
            return False
        except StopIteration:
            return True


def f1(input):
    board = Board(input)
    done = board.take_steps()
    return len(set(s[:2] for s in done))


def f2(input):
    board = Board(input)
    original_guard = board.guard
    seen = set(s[:2] for s in board.take_steps())

    # can not be starting point
    seen.remove(original_guard[:2])

    succesfull_blocks = set()
    while len(seen):
        x, y = seen.pop()
        board.guard = original_guard
        assert board.board[y][x] == '.'
        board.board[y][x] = '#'
        if board.has_loop():
            succesfull_blocks.add((x, y))
        board.board[y][x] = '.'

    return len(succesfull_blocks)
