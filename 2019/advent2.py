import operator


def run(mem):
    sp = 0

    while True:
        opcode = mem[sp]
        if opcode == 99:
            break
        elif opcode in (1, 2):
            op = operator.mul if opcode == 2 else operator.add
            mem[mem[sp + 3]] = op(mem[mem[sp + 1]], mem[mem[sp + 2]])
            sp += 4
        else:
            print("Error")
            break
    return mem[0]


def f1(input):
    mem = [int(s) for s in input[0].split(",")]
    run(mem)


def f2(input):
    if len(input[0]) < 100:
        return
    mem = [int(s) for s in input[0].split(",")]

    for i in range(100):
        for j in range(100):
            mem[1] = i
            mem[2] = j

            if run(mem[::]) == 19690720:
                return 100 * i + j
