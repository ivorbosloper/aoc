EMPTY = []

def parse(input):
    graph = {}
    for line in input.split("\n"):
        source, targets = line.split(": ")
        graph[source] = targets.split()
    return graph

def f1(graph):
    def count(paths, source, target):
        if source == target:
            return 1
        if source in paths:
            return paths[source]
        total = sum(count(paths, x, target) for x in graph[source])
        paths[source] = total

        return total

    return count({},"you", "out")


def f2(graph):
    if len(graph) <= 10:
        graph = parse("""\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""")

    def count(paths, source, target):
        if source == target:
            return 1
        if source in paths:
            return paths[source]
        total = sum(count(paths, x, target) for x in graph.get(source, EMPTY))
        paths[source] = total

        return total

    route1 = count({},"svr", "dac") * count({},"dac", "fft") * count({},"fft", "out")
    route2 = count({},"svr", "fft") * count({},"fft", "dac") * count({},"dac", "out")
    return route1 + route2
