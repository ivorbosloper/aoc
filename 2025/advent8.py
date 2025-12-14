from math import sqrt

def parse_line(line):
    return tuple(map(int, line.split(",")))

def f1(positions):
    stop_at = (10 if len(positions) < 50 else 1000)
    distances = [[0 for __ in positions] for _ in positions]
    srt = []
    for i, e1 in enumerate(positions):
        for j in range(0, i):
            e2 = positions[j]
            dist = sqrt(sum((_e1-_e2)**2 for _e1, _e2 in zip(e1, e2)))
            distances[i][j] = distances[j][i] = dist
            srt.append((dist, i, j))

    srt.sort()
    circuits = {i: {i} for i in range(len(positions))}
    for dist, i, j in srt[:stop_at]:
        if i in circuits[j]:
            assert circuits[j] == circuits[i]
            continue
        # print(f"Merging {positions[i]} - {positions[j]} (dist = {dist})")
        circuits[j] |= circuits[i]
        for u in circuits[i]:
            circuits[u] = circuits[j]

    sizes = []
    handled = set()
    for i in range(len(positions)):
        if i in handled:
            continue
        sizes.append(len(circuits[i]))
        handled |= circuits[i]
    assert len(handled) == len(positions)
    assert sum(sizes) == len(positions)
    sizes.sort()
    result = sizes[-1] * sizes[-2] * sizes[-3]
    return result

def f2(positions):
    distances = [[0 for __ in positions] for _ in positions]
    srt = []
    for i, e1 in enumerate(positions):
        for j in range(0, i):
            e2 = positions[j]
            dist = sqrt(sum((_e1-_e2)**2 for _e1, _e2 in zip(e1, e2)))
            distances[i][j] = distances[j][i] = dist
            srt.append((dist, i, j))

    srt.sort()
    circuits = {i: {i} for i in range(len(positions))}
    groups = len(positions)
    for dist, i, j in srt:
        if i in circuits[j]:
            assert circuits[j] == circuits[i]
            continue
        # print(f"Merging {positions[i]} - {positions[j]} (dist = {dist})")
        circuits[j] |= circuits[i]
        for u in circuits[i]:
            circuits[u] = circuits[j]
        groups -= 1
        if groups == 1:
            return positions[i][0] * positions[j][0]
