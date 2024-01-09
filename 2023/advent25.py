from collections import defaultdict
from email.policy import default
from itertools import islice

import graphviz


def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def f1_viz(input):
    g = graphviz.Graph(name="test")
    for line in input:
        n = line.split(":")[0]
        g.node(n, n)
    for line in input:
        n, edges = line.split(": ")
        for e in edges.split(" "):
            g.edge(n, e)
    print(g.source)
    g.render(f"test{len(input)}.gv", view=True, engine="neato")
    # visually find the 3 nodes to cut
    """jhq - zkt
       vph - tjz
       pgt - lnr"""


def f1(input):
    if len(input) < 30:
        return
    g: dict[str, set[str]] = defaultdict(set)
    for line in input:
        n, edges = line.split(": ")
        edges = edges.split(" ")
        g[n].update(set(edges))
        for e in edges:
            g[e].add(n)

    for c1, c2 in batched(("jhq,zkt,vph,tjz,pgt,lnr").split(","), 2):
        print(c1, c2)
        g[c1].remove(c2)
        g[c2].remove(c1)

    reached = set()
    to_test = set(["jhq"])
    while to_test:
        n = to_test.pop()
        if n not in reached:
            reached.add(n)
            to_test.update(g[n])
    # 547410
    return len(reached) * (len(g) - len(reached))
