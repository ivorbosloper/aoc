
def f1(input):
    mask_or = mask_and = None
    mem = {}
    for line in input:
        cmd, arg = line.split(" = ")
        if cmd == 'mask':
            mask_or = int(arg.replace('X', '0'), 2)
            mask_and = int(arg.replace('X', '1'), 2)
        else:
            address = int(cmd[4:-1])
            mem[address] = int(arg) & mask_and | mask_or

    return sum(mem.values())


def f2(input):
    mask_or = mask_and = None
    mem = {}
    for line in input:
        cmd, arg = line.split(" = ")
        if cmd == 'mask':
            mask_or = int(arg.replace('X', '0'), 2)
            mask_and = int(arg.replace('X', '1'), 2)
        else:
            address = int(cmd[4:-1])
            mem[address] = int(arg) & mask_and | mask_or

    return sum(mem.values())
