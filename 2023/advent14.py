from util import BaseBoard

# N, E, S, W (x, y)
HV_VARIANTS = ((0, -1), (-1, 0), (0, 1), (1, 0))
N, W, S, E = HV_VARIANTS


def swap_range(stop, step):
    return (0, stop, step) if step > 0 else (stop - 1, -1, step)


class Board(BaseBoard):
    def tilt(self, direction=N):
        board = self.board
        if direction[0]:  # move over x
            lv1 = swap_range(self.width, -direction[0])
            lv2 = 0, self.height
        else:
            lv1 = swap_range(self.height, -direction[1])
            lv2 = 0, self.width
        for l1 in range(*lv1):
            for l2 in range(*lv2):
                x, y = (l1, l2) if direction[0] else (l2, l1)
                block = board[y][x]
                if block in "#O" or self.get(x + direction[0], y + direction[1]) == ".":
                    continue
                assert block == "."
                # now scan down until you find an O (or stop on something else)
                nx, ny = x - direction[0], y - direction[1]
                while self.get(nx, ny) == ".":
                    nx, ny = nx - direction[0], ny - direction[1]
                found = self.get(nx, ny, "#")
                if found == "#":
                    continue
                assert found == "O"
                board[y][x] = "O"
                board[ny][nx] = "."

    def weight(self):
        return sum(
            (self.height - y)
            for x in range(self.width)
            for y in range(self.height)
            if self.board[y][x] == "O"
        )


def f1(input):
    board = Board(input)
    board.tilt(direction=N)
    return board.weight()


def f2(input):
    max_cycle = 1000000000
    board = Board(input)
    states = {}
    counter = 0

    # print()
    # print(board)

    while True:
        key = str(board)
        if key in states:
            break
        for direction in HV_VARIANTS:
            board.tilt(direction)
        states[key] = counter
        counter += 1

    # we're now at counter, which is a loop back to states[key]
    steps_left = (max_cycle - states[key]) % (counter - states[key])
    print(counter, states[key], f"up to {max_cycle} still", steps_left)
    for _ in range(steps_left):
        for direction in HV_VARIANTS:
            board.tilt(direction)
    # too high 90201
    return board.weight()
