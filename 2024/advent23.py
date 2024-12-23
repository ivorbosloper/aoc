from collections import defaultdict

def parse(inp):
    graph = defaultdict(set)
    for line in inp.split("\n"):
        n1, n2 = line.split("-")
        graph[n1].add(n2)
        graph[n2].add(n1)
    return graph

def combinations(graph):
    ts = set(n for n in graph if n[0] == 't')
    # for n1, n2, n3 in combinations(graph, 3):
    for n1 in graph:
        for n2 in graph[n1]:
            if n2 < n1:
                continue  # one ordering only
            for n3 in graph[n2]:
                if n3 < n2:
                    continue  # one ordering only
                if n3 not in graph[n1]:
                    continue  # should be triangle
                if n1 in ts or n2 in ts or n3 in ts:
                    yield n1, n2, n3

def f1(graph):
    return sum(1 for _ in combinations(graph))


def f2(graph):
    groups, new_groups = None, {frozenset({n}) for n in graph}  # avoid unhashable with frozenset
    while new_groups:
        # generate all new groups with 1 extra element
        groups = new_groups
        new_groups = {group|{n} for group in groups for n, nodes in graph.items() if group.issubset(nodes)}
    print(','.join(sorted(next(iter(groups)))))


# def f2(graph):
#     import networkx as nx
#     g = nx.Graph()
#     g.add_edges_from([start, end] for start, connections in graph.items() for end in connections)
#     largest = []
#     for clique in nx.find_cliques(g):
#         if len(clique) > len(largest):
#             largest = clique
#     return ",".join(sorted(largest))