HV_VARIANTS = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIR = dict(zip("URDL", HV_VARIANTS))


class Line:
    def __init__(self, moves=None) -> None:
        self.step = 0
        self.pos = (0, 0)
        self.visited: map[(int, int)] = {}
        if moves:
            for m in moves:
                self.move(m)

    def move(self, m):
        direction = DIR[m[0]]
        steps = int(m[1:])
        for _ in range(steps):
            self.step += 1
            self.pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
            self.visited.setdefault(self.pos, self.step)


def f1(input):
    line1, line2 = (Line(i.split(",")) for i in input)
    intersections = set(line1.visited).intersection(set(line2.visited))
    return min(abs(p[0]) + abs(p[1]) for p in intersections)


def f2(input):
    line1, line2 = (Line(i.split(",")) for i in input)
    intersections = set(line1.visited).intersection(set(line2.visited))
    return min(line1.visited[p] + line2.visited[p] for p in intersections)
