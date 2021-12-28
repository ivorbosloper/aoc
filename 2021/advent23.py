import operator
import sys
from functools import reduce
from queue import PriorityQueue
from collections import defaultdict

ENERGY = [1, 10, 100, 1000]


class Board:
    def __init__(self, input):
        self.solved = []
        self.board = []
        self.target_columns = []
        self.target_rows = []
        self.length = len(input) - 3  # 2 or 4
        self.hall_row = 1
        assert self.length in (2, 4)
        abcd = [None] * (4 * self.length)
        for y, row in enumerate(input):
            r = []
            for x, c in enumerate(row):
                if c in 'ABCD':
                    i = (ord(c) - ord('A')) * self.length
                    while abcd[i]:
                        i += 1
                    abcd[i] = y, x
                    c = '.'
                r.append(c)
            self.board.append(r)

        self.abcd = self.sorted(abcd)
        self.target_columns = sorted(set(x for y, x in abcd))
        self.target_rows = sorted(set(y for y, x in abcd))
        self.solved = tuple(
            (self.target_rows[i % self.length], self.target_columns[i // self.length])
            for i in range(self.length * 4))
        assert self.sorted(self.solved) == self.solved, f"{self.sorted(self.solved)} != {self.solved}"

    def sorted(self, t):
        if len(set(t)) != len(t):
            raise AssertionError(f"Duplicate elements {t}")
        return tuple(reduce(operator.add, (sorted(t[i*self.length:(i+1) * self.length]) for i in range(4))))

    def pos_map(self, abcd=None):
        return {v: chr(ord('A') + i//self.length) for i, v in enumerate(abcd or self.abcd)}

    def to_string(self, abcd=None):
        m = self.pos_map(abcd)
        return "\n".join("".join(m.get((y, x), e) for x, e in enumerate(row)) for y, row in enumerate(self.board))

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return str(self)

    def get_options(self, index, abcd):
        source = abcd[index]
        b_index = index // self.length
        t_col = self.target_columns[b_index]
        if source[0] != self.hall_row:  # still/already below
            if (source[0]-1, source[1]) in abcd:
                return  # go up is blocked
            if source[1] == t_col and all(s[1] != t_col or b_index == i//self.length for i, s in enumerate(abcd)):
                return  # in target_column, everything in column is same kind, don't move

            # still below, got to move
            new_y = self.hall_row
            steps_up = source[0] - new_y
            for sign in (-1, 1):
                for x in range(1, 12):
                    new_x = source[1] + sign * x
                    if new_x in self.target_columns:
                        continue  # can not park at entrance

                    new_pos = new_y, new_x
                    if not (0 < new_x < len(self.board[0]) and self.board[new_y][new_x] == '.') or new_pos in abcd:
                        break  # blocked, stop moving forward
                    yield steps_up + x, new_pos
            return

        # in hallway, can only move directly to target (or not)
        if any(s[1] == t_col and i//self.length != b_index for i, s in enumerate(abcd)):
            return  # some other amiphod in target row

        sign = -1 if t_col < source[1] else 1
        if any((source[0], x) in abcd for x in range(source[1] + sign, t_col, sign)):
            return  # something is blocking our way to move to the correct pillar

        target_row = min((s[0]-1 for s in abcd if s[1] == t_col), default=self.target_rows[-1])
        yield abs(t_col - source[1]) + (target_row - source[0]), (target_row, t_col)

    def shortest_path(self):
        queue = PriorityQueue()
        cost = defaultdict(lambda: sys.maxsize)
        cost[self.abcd] = 0
        queue.put((0, self.abcd))
        fastest = sys.maxsize

        while not queue.empty():
            current_cost, abcd = queue.get()
            if current_cost > cost[abcd] or current_cost >= fastest:  # passed by a quicker one
                continue
            if abcd == self.solved:
                if fastest > current_cost:
                    fastest = current_cost
                continue
            for i, amiphod in enumerate(abcd):  # try to move any amipod, generating a new situation
                for steps, pos in self.get_options(i, abcd):
                    # print(f"moving {chr(ord('A') + i//2)} {i}:{amiphod} to {pos} in {steps} steps")
                    new_cost = current_cost + steps * ENERGY[i//self.length]
                    new_abcd = self.sorted([pos if ai == i else a for ai, a in enumerate(abcd)])
                    if new_cost >= cost[new_abcd]:
                        continue
                    cost[new_abcd] = new_cost
                    queue.put((new_cost, new_abcd))
                    # new_board = self.to_string(new_abcd).split('\n')
                    # print(f">>>> {steps} for {chr(ord('A') + i//self.length)}, costing {new_cost - current_cost} --> {new_cost} {new_board[1][1:12]} {new_abcd}")
                    # print("\n".join(f"{a} {b}" for a, b in zip(self.to_string(abcd).split('\n'), new_board)))
        return fastest


def f1(input):
    print()
    b = Board(input)
    print(b)
    fastest = b.shortest_path()
    return fastest


def f2(input):
    return f1(input[:3] + ["###D#C#B#A###", "###D#B#A#C###"] + input[3:])
