import sys
from queue import PriorityQueue
from collections import defaultdict

ENERGY = [1, 10, 100, 1000]


class Board:
    def __init__(self, input=None):
        self.abcd = tuple((0, 0) for _ in range(8))
        self.solved = []
        self.board = []
        self.target_columns = []
        self.target_rows = []
        if not input:
            return

        abcd = [None] * 8
        for y, row in enumerate(input):
            r = []
            for x, c in enumerate(row):
                if c in 'ABCD':
                    i = (ord(c) - ord('A')) * 2
                    if abcd[i]:
                        i += 1
                    abcd[i] = y, x
                    c = '.'
                r.append(c)
            self.board.append(r)

        self.abcd = tuple(abcd)
        self.target_columns = sorted(set(x for y, x in abcd))
        self.target_rows = sorted(set(y for y, x in abcd))

        # generate all 'solved' states, as aabbccdd has multiple valid permutations
        self.solved = set(tuple(
            (self.target_rows[1 if (i & (1 << c//2)) ^ (c % 2) else 0], self.target_columns[c//2])
            for c in range(8)) for i in range(16))

        assert len(self.solved) == 16

    def pos_map(self, abcd=None):
        return {v: chr(ord('A') + i//2) for i, v in enumerate(abcd or self.abcd)}

    def to_string(self, abcd=None):
        m = self.pos_map(abcd)
        return "\n".join("".join(m.get((y, x), e) for x, e in enumerate(row)) for y, row in enumerate(self.board))

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return str(self)

    def get_options(self, index, abcd):
        source = abcd[index]
        t_col = self.target_columns[index // 2]
        if source[0] in self.target_rows:  # still/already below
            if source[1] == t_col and (self.target_rows[1], source[1]) in abcd[index*2:index*2+2]:
                return  # already at target, don't do anything
            # still below, got to move
            if source[0] == self.target_rows[1] and (self.target_rows[0], source[1]) in abcd:
                return  # go up is blocked
            new_y = self.target_rows[0] - 1
            steps_up = source[0] - new_y
            for sign in (-1, 1):
                for x in range(1, 12):
                    new_x = source[1] + sign * x
                    new_pos = new_y, new_x
                    if not (0 < new_x < len(self.board[0]) and self.board[new_y][new_x] == '.') or new_pos in abcd:
                        break  # blocked, stop moving forward
                    if new_x in self.target_columns:
                        continue  # can not park at entrance
                    yield steps_up + x, new_pos
            return

        # in hallway, can only move directly to target (or not)
        if (self.target_rows[0], t_col) in abcd: return  # top not empty
        go_to_bottom = True
        if (self.target_rows[1], t_col) in abcd:
            if abcd.index((self.target_rows[1], t_col))//2 != index // 2:
                return  # only other same-letter-amiphod is allowed
            go_to_bottom = False

        sign = -1 if t_col < source[1] else 1
        if any((self.target_rows[0], x) in abcd for x in range(source[1], t_col, sign)):
            return  # something is blocking our way to move to the correct pillar
        yield abs(t_col - source[1]) + (2 if go_to_bottom else 1), (self.target_rows[int(go_to_bottom)], t_col)

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
            if abcd in self.solved:
                if fastest > current_cost:
                    fastest = current_cost
                continue
            for i, amiphod in enumerate(abcd):  # try to move any amipod, generating a new situation
                # print(f"trying to move {chr(ord('A') + i//2)} {i}:{amiphod}")
                for steps, pos in self.get_options(i, abcd):
                    # print(f"moving {chr(ord('A') + i//2)} {i}:{amiphod} to {pos} in {steps} steps")
                    new_cost = current_cost + steps * ENERGY[i//2]
                    new_abcd = tuple(pos if ai == i else a for ai, a in enumerate(abcd))
                    if new_cost >= cost[new_abcd]:
                        # breakpoint()
                        continue
                    cost[new_abcd] = new_cost
                    queue.put((new_cost, new_abcd))
                    # new_board = self.to_string(new_abcd).split('\n')
                    # print(f">>>> {steps} for {chr(ord('A') + i//2)}, costing {new_cost - current_cost} --> {new_cost} {new_board[1][1:12]} {new_abcd}")
                    # print("\n".join(f"{a} {b}" for a, b in zip(self.to_string(abcd).split('\n'), new_board)))
            # print('---')
        return fastest

def f1(input):
    print()
    b = Board(input)
    print(b)
    fastest = b.shortest_path()
    return fastest
