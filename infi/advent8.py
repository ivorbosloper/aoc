from collections import deque

VARIANTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def parse_line(line):
    return line.split(" ")


class Machine:
    def __init__(self, input):
        self.input = input
        self.pc = 0
        self.stack = []

    def start(self, pos: tuple[int, int, int]):
        self.pc = 0
        self.stack = []
        while True:
            instruction = self.input[self.pc]
            # print(instruction, self.pc, list(reversed(self.stack)))
            opcode = instruction[0]
            if opcode == 'push':
                try:
                    v = pos["XYZ".index(instruction[1])]
                except ValueError:
                    v = int(instruction[1])
                self.stack.append(v)
            elif opcode == 'add':
                v = self.stack.pop()
                self.stack[-1] += v
            elif opcode == 'jmpos':
                if self.stack.pop() >= 0:
                    self.pc += int(instruction[1])
            else:
                assert opcode == 'ret', f"invalid opcode {opcode}"
                return self.stack[-1]
            self.pc += 1


def f1(input):
    m = Machine(input)
    total = 0
    for x in range(30):
        for y in range(30):
            for z in range(30):
                total += m.start((x, y, z))
    return total


def f2(input):
    m = Machine(input)
    space = [[[m.start((x, y, z)) > 0 for x in range(30)] for y in range(30)] for z in range(30)]
    sgroup = [[[None for _x in range(30)] for _y in range(30)] for _z in range(30)]
    group_count = 0

    def color_nodes_from(z, y, x):
        q = deque([(z, y, x)])
        while q:
            z, y, x = q.pop()
            # print("dequeue", group_count, z, y, x)
            # assert space[z][y][x] and not sgroup[z][y][x]
            sgroup[z][y][x] = group_count
            for dz, dy, dx in VARIANTS:
                nz, ny, nx = z + dz, y + dy, x + dx
                if 0 <= nz < 30 and 0 <= ny < 30 and 0 <= nx < 30 \
                        and space[nz][ny][nx] and not sgroup[nz][ny][nx]:
                    q.append((nz, ny, nx))

    for z in range(30):
        for y in range(30):
            for x in range(30):
                if space[z][y][x] and not sgroup[z][y][x]:
                    group_count += 1
                    # do a new search from this point for all reachable nodes
                    color_nodes_from(z, y, x)

    return group_count
