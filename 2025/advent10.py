import re
from dataclasses import dataclass

@dataclass
class Machine:
    target: int
    buttons: list[tuple[int, ...]]
    jolts: tuple[int, ...]

    def cost_target(self):
        paths = [sum(2**n for n in btn) for btn in self.buttons]
        fastest = {0: 0}
        front = {0}
        while True:
            # print(front)
            new_front = set()
            assert len(front)
            for state in front:
                cost = fastest[state]
                if state == self.target:
                    return cost
                for switch in paths:
                    c = state ^ switch
                    if c in fastest:
                        continue
                    fastest[c] = cost + 1
                    new_front.add(c)
            front = new_front

    # Naive Approach. Search space is way to high. Should factor out steps...
    # btn3+btn1+btn0 = 134
    # btn2+btn5+btn8 = 255
    # solve for minimal(btn1+btn2+btn3+...)
    def jolt_target(self):
        print(self)
        initial = tuple(0 for _ in self.jolts)
        fastest = {initial: 0}
        front = {initial}
        while True:
            # print(front)
            new_front = set()
            assert len(front)
            for state in front:
                cost = fastest[state]
                if state == self.jolts:
                    return cost

                for btn in self.buttons:
                    new_state = tuple(s + (i in btn) for i, s in enumerate(state))
                    if new_state in fastest:
                        continue
                    # cut-off condition; all jolts should be lower than target
                    if any(j1>j2 for j1, j2 in zip(new_state, self.jolts)):
                        continue
                    fastest[new_state] = cost + 1
                    new_front.add(new_state)
            front = new_front

    def jolt_target2(self):
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()

        vars = []
        adds_to_counter = [[] for _ in self.jolts]
        for index, btn in enumerate(self.buttons):
            mx = min(self.jolts[b] for b in btn)
            vars.append(model.new_int_var(0, mx, f"btn_{index}"))

            for b in btn:
                adds_to_counter[b].append(index)

        for lst, jolt in zip(adds_to_counter, self.jolts):
            model.add(sum(vars[i] for i in lst) == jolt)

        model.minimize(sum(vars))

        solver = cp_model.CpSolver()
        status = solver.solve(model)
        assert status in [cp_model.OPTIMAL, status == cp_model.FEASIBLE]
        return sum(solver.value(v) for v in vars)


def parse_line(line):
    m = re.match(r"\[([.#]+)] (.*?) {(.*)}$", line)

    target = int(''.join(reversed(['0' if c == '.' else '1' for c in m.group(1)])), 2)
    buttons = [tuple(int(n) for n in x[1:-1].split(',')) for x in m.group(2).split()]
    jolts = tuple(int(_) for _ in m.group(3).split(','))
    return Machine(target, buttons, jolts)


def f1(machines: list[Machine]):
    return sum(m.cost_target() for m in machines)

def f2(machines: list[Machine]):
    return sum(m.jolt_target2() for m in machines)
