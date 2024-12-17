import re

class Machine:
    def __init__(self, inp):
        for line in inp.splitlines():
            if m := re.match(r'Register ([A-C]): (\d+)', line):
                # print(m.group(1), '=', m.group(2))
                setattr(self, m.group(1), int(m.group(2)))
            elif m := re.match("Program: (.*)", line):
                # print(m.group(1))
                self.program = [int(a) for a in m.group(1).split(',')]

    def run(self):
        out = []
        pc = 0
        r = {k: getattr(self, k) for k in 'ABC'}

        def combo(a):
            return a if a <= 3 else r["ABC"[a-4]]

        while pc < len(self.program):
            op, arg = self.program[pc:pc+2]
            # print(f"{pc:3d}:, {op}, {arg} ({combo(arg)}). A={r['A']} C={r['B']} C={r['C']} - {','.join(out)}")
            if op == 0:
                r['A'] = r['A'] // 2 ** combo(arg)
            elif op == 1:
                r['B'] = r['B'] ^ arg
            elif op == 2:
                r['B'] = combo(arg) % 8
            elif op == 3:
                if r['A'] > 0:
                    pc = arg
                    continue
            elif op == 4:
                r['B'] = r['B'] ^ r['C']
            elif op == 5:
                out.append(str(combo(arg) % 8))
            elif op == 6:
                r['B'] = r['A'] // 2 ** combo(arg)
            elif op == 7:
                r['C'] = r['A'] // 2 ** combo(arg)
            pc += 2
        return ','.join(out)

    def run2(self):
        out_index = 0
        pc = 0
        r = {k: getattr(self, k) for k in 'ABC'}

        def combo(a):
            return a if a <= 3 else r["ABC"[a-4]]

        while pc < len(self.program):
            op, arg = self.program[pc:pc+2]
            if op == 0:
                r['A'] = r['A'] // 2 ** combo(arg)
            elif op == 1:
                r['B'] = r['B'] ^ arg
            elif op == 2:
                r['B'] = combo(arg) % 8
            elif op == 3:
                if r['A'] > 0:
                    pc = arg
                    continue
            elif op == 4:
                r['B'] = r['B'] ^ r['C']
            elif op == 5:
                if out_index >= len(self.program) or combo(arg) % 8 != self.program[out_index]:
                    return False
                out_index += 1
            elif op == 6:
                r['B'] = r['A'] // 2 ** combo(arg)
            elif op == 7:
                r['C'] = r['A'] // 2 ** combo(arg)
            pc += 2
        return out_index == len(self.program)

    def run3(self):
        i = 0
        length = len(self.program)
        while True:
            i += 1
            a, b, c, oi = i, 0, 0, 0
            while a and oi < length:
                b = a % 8
                b = b ^ 5
                c = a // 2 ** b
                b = b ^ 6
                a = a // 8
                b = b ^ c
                if b % 8 != self.program[oi]:
                    break
                oi += 1
            if a == 0 and oi == length:
                return i

    def solve(self, index, built_up):  # index, target_a
        if index < 0:
            return built_up  # built_up found at the beginning of the program

        def combo(argument):
            return argument if argument <= 3 else (a, b, c)[argument - 4]

        for new_bits in range(8):
            new_built_up = built_up * 8 + new_bits  # insert 3 new bits and test if it works
            a, b, c, pc = new_built_up, 0, 0, 0
            outcome = None
            while outcome is None and pc < len(self.program):
                op, arg = self.program[pc:pc + 2]
                match op:
                    case 0:
                        a = a // 2 ** combo(arg)
                    case 1:
                        b = b ^ arg
                    case 2:
                        b = combo(arg) % 8
                    case 3:
                        pc = arg - 2 if a != 0 else pc
                    case 4:
                        b = b ^ c
                    case 5:
                        outcome = combo(arg) % 8
                    case 6:
                        b = a // 2 ** combo(arg)
                    case 7:
                        c = a // 2 ** combo(arg)
                    case _:
                        assert False, f"Unexpected op {op}"
                pc += 2

            if outcome == self.program[index]:
                result = self.solve(index - 1, new_built_up)
                if result is not None:
                    return result


def parse(input):
    return Machine(input)


def f1(m):
    print()
    return m.run()


# def f2(m):
#     return m.run3()

# def f2(m):
#     m.A = 0
#     while True:
#         m.A += 1
#         print(f"\r Running... {m.A}", end="")
#         if m.run2():
#             print()
#             return m.A

def f2(m):
    return m.solve(len(m.program)-1, 0)
