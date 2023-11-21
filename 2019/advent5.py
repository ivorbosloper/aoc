import operator


def run(mem, inp):
    sp = 0
    out = []

    while True:
        opcode = mem[sp] % 100
        rest = mem[sp] // 100
        modes = rest % 10, (rest // 10) % 10

        # print(f"[{sp}]:{mem[sp:sp+4]} {opcode}:{modes}")
        if opcode == 99:
            break
        elif opcode in (1, 2):
            op = operator.mul if opcode == 2 else operator.add
            p1 = sp + 1 if modes[0] else mem[sp + 1]
            p2 = sp + 2 if modes[1] else mem[sp + 2]
            mem[mem[sp + 3]] = op(mem[p1], mem[p2])
            sp += 4
        elif opcode == 3:
            mem[mem[sp + 1]] = next(inp)
            sp += 2
        elif opcode == 4:
            p1 = sp + 1 if modes[0] else mem[sp + 1]
            out.append(mem[p1])
            sp += 2
        elif opcode in (5, 6):
            p1 = sp + 1 if modes[0] else mem[sp + 1]
            p2 = sp + 2 if modes[1] else mem[sp + 2]
            sp += 3
            if bool(mem[p1]) == (opcode == 5):
                sp = mem[p2]
        elif opcode in (7, 8):
            op = operator.lt if opcode == 7 else operator.eq
            p1 = sp + 1 if modes[0] else mem[sp + 1]
            p2 = sp + 2 if modes[1] else mem[sp + 2]
            mem[mem[sp + 3]] = 1 * op(mem[p1], mem[p2])
            sp += 4
        else:
            print("Error")
            break
    return out


def f1(input):
    mem = [int(s) for s in input[0].split(",")]
    return run(mem, iter([1]))


def f2(input):
    mem = [int(s) for s in input[0].split(",")]
    return run(mem, iter([5]))
