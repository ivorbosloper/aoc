from itertools import pairwise

OPTS = (
    (1,0,0), (-1,0,0),
    (0,1,0), (0,-1,0),
    (0,0,1), (0,0,-1),
)

def parse_line(line):
    return tuple(map(int, line.split(',')))

def add(p1, p2):
    return tuple(i+j for i, j in zip(p1, p2))

def f1(points):
    graph = set(points)
    return sum(1 for p in points for j in OPTS if add(p, j) not in graph)

def f2(points):
    graph = set(points)
    min_d = tuple(min(p[i] for p in points) for i in range(3))
    max_d = tuple(max(p[i] for p in points) for i in range(3))

    def valid_point(p):
        return p not in graph and \
            all(min_d[i]-1 <= p[i] <= max_d[i]+1 for i in range(3))

    color = {}   # place -> color
    real_color = {} # color --> real_color
    color_nr = -1

    start_points = set(add(p, j) for p in points for j in OPTS if add(p, j) not in graph)
    for point in start_points:
        if point in color:
            continue
        assert point not in graph
        # start painting from here in new color
        queue = [point]
        color_nr += 1
        real_color[color_nr] = color_nr     
        while len(queue):
            p = queue.pop()
            clr = color.get(p)
            if clr is not None:
                if clr != color_nr:  # never happens (?)
                    print(f"point {point} recolor color {color_nr} --> {clr}")
                    assert clr < color_nr
                    real_color[color_nr] = clr
            else:
                color[p] = color_nr
                tested = [add(p, j) for j in OPTS if add(p, j) not in graph]
                new_stuff = [add(p, j) for j in OPTS if valid_point(add(p, j))]
                queue.extend(new_stuff)

    assert min_d not in graph  # just a guess, any point on the outside would work
    real_outside_color = real_color[color[min_d]]
    print(sum(1 for p in points for j in OPTS if add(p, j) not in graph and real_color[color[add(p, j)]] == real_outside_color))
