from collections import defaultdict


def parse_line(x):
    return x.split(")")


def f1(input):
    graph = defaultdict(list)
    for k, v in input:
        graph[k].append(v)

    # def recurse(k, depth=0):
    #     print(k, depth)
    #     return depth + (
    #         sum(recurse(child, depth + 1) for child in graph[k]) if k in graph else 0
    #     )
    # return recurse("COM")

    queue = [("COM", 0)]
    result = 0
    while queue:
        node, depth = queue.pop()
        # print(node, depth)
        result += depth
        if node in graph:
            for child in graph[node]:
                queue.append((child, depth + 1))
    return result


def f2(input):
    if len(input) < 20:
        input = [
            parse_line(l)
            for l in """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".split(
                "\n"
            )
        ]
    graph = defaultdict(list)
    for k, v in input:
        graph[v].append(k)
        graph[k].append(v)

    shortest = {}
    queue = [("YOU", 0)]
    while queue:
        node, steps = queue.pop()
        if node in shortest:
            continue
        shortest[node] = steps
        for child in graph[node]:
            queue.append((child, steps + 1))

    return shortest["SAN"] - 2
