def parse_line(line):
    instruction, arg = line.split(' ')
    return instruction, int(arg)


def interpret(instructions):
    pc, acc = 0, 0
    visited = len(instructions) * [False]
    while True:
        if pc < 0:
            return "pc<0", acc
        elif pc == len(instructions):
            return "finished", acc
        if visited[pc]:
            return "loop", acc
        instruction, arg = instructions[pc]
        visited[pc] = True
        if instruction == 'acc':
            acc += arg
        elif instruction == 'jmp':
            pc = pc + arg
            continue
        pc += 1

def f1(input):
    reason, value = interpret(input)
    assert reason == 'loop'
    return value


def f2(input):
    for line_nr in range(len(input)):
        if input[line_nr][0] in ('jmp', 'nop'):
            copy = [x[:] for x in input]
            copy[line_nr] = 'jmp' if copy[line_nr][0] == 'nop' else 'nop', copy[line_nr][1]
            reason, value = interpret(copy)
            if reason == 'finished':
                return value

