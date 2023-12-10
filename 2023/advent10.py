from itertools import chain

from util import BaseBoard

DIRN = "RDLU"
DIRV = ((1, 0), (0, 1), (-1, 0), (0, -1))
MAPPING = dict(zip(DIRN, DIRV))

CHARS = {
    "|": "UD",
    "-": "LR",
    "L": "UR",
    "J": "UL",
    "7": "DL",
    "F": "DR",
    ".": "",
    "S": "",
}


class Board(BaseBoard):
    def find(self, letter):
        return next(
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if self.board[y][x] == letter
        )

    def path(self, pos):
        pointer = 0
        stack_pos = [pos] + [None] * 100000
        stack_vindex = [-1] + [None] * 100000
        while pointer >= 0:
            stack_vindex[pointer] += 1
            # print(pointer, stack_pos[: pointer + 1], stack_vindex[: pointer + 1])
            dir = stack_vindex[pointer]
            pos = stack_pos[pointer]
            cur_c = self.board[pos[1]][pos[0]]
            if dir >= 4:
                pointer -= 1
                continue
            if pointer > 0:
                if stack_vindex[pointer - 1] == (dir + 2) % 4:
                    # don't go straight back
                    continue
                if DIRN[dir] not in CHARS[cur_c]:
                    # Next move should be allowed
                    continue

            dv = DIRV[dir]
            next_pos = (pos[0] + dv[0], pos[1] + dv[1])
            next_c = self.get(*next_pos, ".")
            if next_c == "S":
                # print(pointer, stack_pos[: pointer + 1], stack_vindex[: pointer + 1])
                return stack_pos[: pointer + 1]
            next_accepts = CHARS[next_c]
            should_contain = DIRN[(dir + 2) % 4]

            if should_contain not in next_accepts:
                continue

            pointer += 1
            stack_pos[pointer] = next_pos
            stack_vindex[pointer] = -1

    def odd_count(self, path):
        # do a horizontal line scan, keep track of inside/outside
        # color the area's even/odd based on crossings
        # just like polygon_area even/odd
        # count '.' in the odd area's
        # F----7 is not a crossing
        # F----J is a crossing
        # L----J is not a crossing
        # L----7 is a crossing
        # | is a crossing

        path = set(path)
        count = 0
        for y, vals in enumerate(self.board):
            odd = False
            push = None
            for x, v in enumerate(vals):
                if (x, y) not in path:
                    if odd:
                        count += 1
                    continue

                if v == "|":
                    odd = not odd
                elif v in ".-":
                    assert bool(push) == (v == "-")
                elif v in "LF":
                    assert not push
                    push = v
                elif v in "7J":
                    assert push
                    if (push == "L" and v == "7") or (push == "F" and v == "J"):
                        odd = not odd
                    push = None
                else:
                    assert False
        return count


def f1(input):
    board = Board(input)
    start = board.find("S")
    return (len(board.path(start)) + 1) // 2


def f2(input):
    board = Board(input)
    start = board.find("S")
    path = board.path(start)

    # quick hack to replace 'S' with proper loop-char
    board.board[start[1]][start[0]] = "7" if board.width < 30 else "F"
    return board.odd_count(path)
