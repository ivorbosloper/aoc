from io import StringIO

def parse(input):
    current = []
    elves = [current]
    for l in StringIO(input):
        l = l.strip()
        if l == "":
            current = []
            elves.append(current)
        else:
            current.append(int(l))
    return elves


def f1(input):
    sizes = [sum(i) for i in input]
    print(max(sizes))

def f1(input):
    sizes = [sum(i) for i in input]
    sizes.sort()
    print(sum(sizes[-3:]))

