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


class TrieNode:
    def __init__(self, mask, value):
        self.mask = mask
        self.value = value
        self.left = self.right = None  # TrieNode

    def merge(self, mask, value):
        pass

    def sum(self):
        factor = 2 ** self.mask.count("X")
        return factor * self.value

    @property
    def depth(self):
        return len(self.mask) + (0 if self.left is None else self.left.depth)


def f2(input):
    mask = "0" * 36
    writes = None

    for line in input:
        cmd, arg = line.split(" = ")
        if cmd == 'mask':
            mask = mask
        else:
            address = f"{int(cmd[4:-1]):036b}"
            w_address = "".join(m if m in '1X' else a for a, m in zip(address, mask))
            if writes is None:
                writes = TrieNode(w_address, int(arg))
            else:
                writes.merge(w_address, int(arg))
    return writes.sum()

