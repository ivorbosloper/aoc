import operator


def run(mem, inp, out):
    sp = 0

    while True:
        opcode = mem[sp] % 100
        rest = mem[sp] // 100
        modes = rest % 10, (rest // 10) % 10

        print(f"[{sp}]:{mem[sp:sp+4]} {opcode}:{modes}")
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
        else:
            print("Error")
            break
    print(out)
    return mem[0]


def f1(input):
    mem = [int(s) for s in input[0].split(",")]
    inp = iter([1])
    out = []
    return run(mem, inp, out)
