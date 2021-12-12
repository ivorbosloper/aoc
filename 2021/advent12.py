from collections import defaultdict


def parse_graph(input):
    graph = defaultdict(set)
    for line in input:
        p1, p2 = line.split("-")
        graph[p1].add(p2)
        graph[p2].add(p1)
    return graph


def parse(input):
    return [block.split("\n") for block in input]


def f1(input):
    for i in input:
        print(f1_real(i))


def f1_real(input):
    graph = parse_graph(input)
    paths_into = defaultdict(int)
    queue = [('start', set())]
    while len(queue):
        p1, visited = queue.pop()
        paths_into[p1] += 1
        if p1.islower():
            visited = visited.copy()
            visited.add(p1)
        for p2 in graph[p1]:
            if p2 not in visited:
                queue.append((p2, visited))
    return paths_into['end']


def f2(input):
    for i in input:
        print(f2_real(i))


def f2_real(input):
    graph = parse_graph(input)
    paths_into = defaultdict(int)
    queue = [('start', defaultdict(int))]
    while len(queue):
        p1, visited = queue.pop()
        paths_into[p1] += 1   # je mag hier dus altijd zijn
        max_links = 1 if any(v == 2 for v in visited.values()) else 2
        if p1.islower():
            visited = visited.copy()
            t = visited[p1] = visited[p1] + 1
            if t > max_links or p1 == 'end':
                continue
        for p2 in graph[p1]:
            if visited[p2] < max_links and p2 != 'start':
                queue.append((p2, visited))
    return paths_into['end']
