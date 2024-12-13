from queue import PriorityQueue
import re
import math

regex = re.compile(r'(Button A|Button B|Prize): X[+=](\d+), Y[+=](\d+)')

class Machine:
    a: tuple[int, int] = None
    b: tuple[int, int] = None
    prize: tuple[int, int] = None

    def __init__(self, inp):
        lines = inp.splitlines()
        assert len(lines) == 3
        for line in lines:
            t, x, y = regex.match(line).groups()
            tpl = (int(x), int(y))
            if t == 'Button A':
                self.a = tpl
            elif t == 'Button B':
                self.b = tpl
            else:
                self.prize = tpl
        assert self.a and self.b and self.prize, inp


def parse(inp):
    return [Machine(machine_inp) for machine_inp in inp.split("\n\n")]


def f1(inp):
    result = 0
    for machine in inp:
        cheapest = {}
        q = PriorityQueue()
        q.put((0, (0, 0)))
        while not q.empty():
            points, tpl = q.get()
            if tpl in cheapest:
                if cheapest[tpl] <= points:
                    continue
            cheapest[tpl] = points
            if tpl == machine.prize:
                result += points
                break
            x, y = tpl
            if x < machine.prize[0] and y < machine.prize[1]:
                q.put((points+3, (x+machine.a[0], y+machine.a[1])))
                q.put((points+1, (x+machine.b[0], y+machine.b[1])))
    print(result)


def f2(inp):
    result = 0
    for m in inp:
        # p = (fa * a[0], fb * b[0])
        # p[0] = fa * a[0] + fb * b[0]
        # p[1] = fa * a[1] + fb * b[1]
        # fa = (p[0] * b[1] - b[0] * p[1]) / (a[0] * b[1] - b[0] * a[1])
        # fb = (p[1] - fa * a[1]) / b[1]
        p = (m.prize[0] + 10000000000000, m.prize[1] + 10000000000000)
        fa = (p[0] * m.b[1] - m.b[0] * p[1]) / (m.a[0] * m.b[1] - m.b[0] * m.a[1])
        fb = (p[1] - fa * m.a[1]) / m.b[1]
        if int(fa) == fa and int(fb) == fb:
            result += int(fa * 3 + fb)
    return result  # too high: 92974408363862, correct 92827349540204
