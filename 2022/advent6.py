def different(s):
    return len(set(s)) == len(s)

def solve(input, nr):
    for line in input:
        for i in range(len(line)-nr):
            if different(line[i:i+nr]):
                print(i+nr)
                break

def f1(input):
    solve(input, 4)

def f2(input):
    solve(input, 14)
