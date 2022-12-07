from io import StringIO
from typing import Tuple

def parse(input):
    current_dir = root = {}
    for line in StringIO(input):
        line = line.strip()
        args = line.split(' ')
        if args[0] != '$':
            size, name = args
            f = {"..": current_dir} if size == 'dir' else int(size)
            current_dir[name] = f
            continue
        if args[1] == 'cd':
            current_dir = root if args[2] == '/' else current_dir[args[2]]
    return root

def calc_sizes(_dir: dict) -> Tuple[int, list[int]]:
    sizes = []
    current_size = 0
    for name, f in _dir.items():
        if name == '..':
            continue
        if isinstance(f, int):
            current_size += f
        else:
            sub_size, sub_sizes = calc_sizes(f)
            sizes.extend(sub_sizes)
            current_size += sub_size
    sizes.append(current_size)
    return current_size, sizes

def f1(fs):
    _, sizes = calc_sizes(fs)
    print(sum(s for s in sizes if s<=100000))

def f2(fs):
    total, sizes = calc_sizes(fs)
    unused_space = (70000000 - total)
    to_free = 30000000 - unused_space
    print(min(s for s in sizes if s >= to_free))
