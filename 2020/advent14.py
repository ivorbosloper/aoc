from itertools import chain, combinations

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


def all_combinations(lst):
    return chain([[]], *(list(combinations(lst, i + 1)) for i in range(len(lst))))


def f2(input):
    mask = "0" * 36
    mem = {}

    for line in input:
        cmd, arg = line.split(" = ")
        if cmd == 'mask':
            mask = arg
        else:
            value = int(arg)
            address = f"{int(cmd[4:-1]):036b}"
            w_address = "".join(m if m in '1X' else a for a, m in zip(address, mask))

            base_address = int(w_address.replace('X', '0'), 2)
            floating = [2**(35-i) for i, c in enumerate(w_address) if c == 'X']
            for cmb in all_combinations(floating):
                mem[base_address + sum(cmb)] = value
    return sum(mem.values())

