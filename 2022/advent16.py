from io import StringIO
import re
from collections import defaultdict

class Node:
    nr: int
    label: str
    rate: int
    links: list

    def __init__(self, nr, label, rate, links):
        self.nr = nr
        self.label = label
        self.rate = rate
        self.links = links


bits = [2**i for i in range(64)]

def parse(input):
    graph = {}
    for line in StringIO(input):
        m = re.match(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line.strip())
        name, rate, links = m.group(1), int(m.group(2)), m.group(3).split(', ')
        graph[name] = Node(len(graph), name, rate, links)
    for name, node in graph.items():
        node.links = tuple(graph[key] for key in node.links)
    return graph

def f1(graph):
    nodes = tuple(graph.values())
    assert [n.nr for n in nodes] == [n for n in range(len(nodes))]

    # state = (location, openstate) --> points
    states = {(graph['AA'].nr, tuple(node.rate == 0 for node in nodes)): 0}  # turn open all 0-value valves
    cycle = 1
    while cycle <= 30:
        print(f"cycle {cycle}, states={len(states)}")
        new_states = {}
        for s, points in states.items():
            location, openstate = s
            score = points + sum(node.rate for index, node in enumerate(nodes) if openstate[index])
            if new_states.get(s, -1) < score: # stay at place
                new_states[s] = score
            if False in openstate:
                node = nodes[location]
                # try open Valve at current location
                if not openstate[node.nr]:
                    new_openstate = tuple(o or index==node.nr for index, o in enumerate(openstate))
                    new_state = location, new_openstate  # valve open
                    if new_states.get(new_state, -1) < score:
                        new_states[new_state] = score
                for node in node.links:
                    new_state = node.nr, openstate
                    if new_states.get(new_state, -1) < score:
                        new_states[new_state] = score
        cycle += 1
        states = new_states
    print(max(v for k,v in states.items()))


def f2(graph):
    nodes = tuple(graph.values())
    assert [n.nr for n in nodes] == [n for n in range(len(nodes))]

    # state = (location1, location2, openstate) --> points
    states = {(graph['AA'].nr, graph['AA'].nr, 
              sum(bits[index] for index, node in enumerate(nodes) if node.rate == 0)): 0}  # turn open all 0-value valves
    complete = bits[len(nodes)] - 1
    cycle = 1
    while cycle <= 26:
        print(f"cycle {cycle}, states={len(states)}")
        new_states = {}

        open_states_per_location = defaultdict(set)
        for (location1, location2, openstate) in states.keys():
            open_states_per_location[(location1, location2)].add(openstate)
        max_points = max(states.values())

        for s, points in states.items():
            location1, location2, openstate = s
            if points < max_points - 100: # estimated guess, come up with a trick to minimize loser-states
                continue
            # if openstate is a subset of other options, skip it. We could have taken a faster path
            if any(openstate | os == os and openstate != os for os in open_states_per_location[location1, location2]):
                continue
            score = points + sum(node.rate for index, node in enumerate(nodes) if openstate & bits[index])
            if new_states.get(s, -1) < score: # all stay at place
                new_states[s] = score
            if openstate != complete:
                for m1 in ("stay", "open") + nodes[location1].links:
                    nlocation1, nopenstate1 = location1, openstate
                    if m1 == 'stay':
                        pass
                    elif m1 == 'open':
                        if openstate & bits[location1]:
                            continue  # can not open, skip option
                        nopenstate1 = openstate + bits[location1]
                    else:  # m1 is Node
                        nlocation1 = m1.nr
                    for m2 in ("stay", "open") + nodes[location2].links:
                        nlocation2, nopenstate2 = location2, nopenstate1
                        if m2 == 'stay':
                            pass
                        elif m2 == 'open':
                            if nopenstate1 & bits[location2]:
                                continue  # can not open
                            nopenstate2 = nopenstate1 + bits[location2]
                        else:  # m2 is Node
                            nlocation2 = m2.nr
                        s = (nlocation1, nlocation2, nopenstate2)
                        if new_states.get(s, -1) < score:
                            new_states[s] = score

        cycle += 1
        states = new_states
    print(max(v for k,v in states.items()))

