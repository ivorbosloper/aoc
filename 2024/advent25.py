def parse(inp):
    locks, keys = [], []
    for schema in inp.split("\n\n"):
        rows = schema.split("\n")
        counts = [sum(rows[y][x] == '#' for y in range(len(rows))) - 1 for x in range(len(rows[0]))]
        if rows[0] == "#####":
            locks.append(counts)
        else:
            keys.append(counts)  # [5-c for c in counts]
    return locks, keys


def f1(inp):
    locks, keys = inp
    matches = 0
    for lock in locks:
        for key in keys:
            m = all(5-lock[x] >= key[x] for x in range(len(lock)))
            if m:
                matches += 1
    return matches
