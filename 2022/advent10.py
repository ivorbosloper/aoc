def parse_line(line):
    return line.split(' ')

POINTS = (20, 60, 100, 140, 180, 220)

def f1(ops):
    total = 0
    x = 1
    pc = 0
    cycle = 0
    running = None
    while(True):
        cycle += 1
        if cycle in POINTS:
            print(cycle, x, x*cycle)  # during cycle X
            total += x * cycle
        if running is not None:
            x += running
            running = None
        else: # fetch new instruction
            if pc >= len(ops):
                break
            op = ops[pc]
            pc += 1
            if op[0] == 'addx':
                running = int(op[1])
    print("signal strength:", total)


def f2(ops):
    pixels = []
    x = 1
    pc = 0
    cycle = 0
    running = None
    while(True):
        pos = cycle % 40
        pixels.append('#' if pos-1 <= x <= pos+1 else '.')
        cycle += 1
        if running is not None:
            x += running
            running = None
        else: # fetch new instruction
            if pc >= len(ops):
                break
            op = ops[pc]
            pc += 1
            if op[0] == 'addx':
                running = int(op[1])

    print("Board", len(pixels))
    print("\n".join(["".join(pixels[i : i+40]) for i in range(0, 240, 40)]))
