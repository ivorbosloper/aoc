DIRECTIONS = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (1, 0),
    'R': (-1, 0)
}

def parse_line(line):
    a = line.split(' ')
    return a[0], int(a[1])

def tabs(t):
    return tuple(abs(e) for e in t)

def do_move(ph, pt):
    difference = (ph[0] - pt[0], ph[1] - pt[1])
    abs_difference = tabs(difference)

    if abs_difference[0] <= 1 and abs_difference[1] <= 1:
        return pt  # already/still touching

    if abs_difference in ((0, 2), (2, 0)):
        # If the head is ever two steps directly up, down, left, or right...
        # ... move one step in that direction
        move = difference[0] // 2, difference[1] // 2
    else:
        # assert abs_difference in ((1, 2), (2, 1))
        move = difference[0] // abs_difference[0], difference[1] // abs_difference[1]
    return pt[0] + move[0], pt[1] + move[1]


def f1(moves):
    ph = pt = 0, 0
    visited = set()

    for d, repeats in moves:
        direction = DIRECTIONS[d]
        for i in range(repeats):
            ph = ph[0] + direction[0], ph[1] + direction[1]
            pt = do_move(ph, pt)
            visited.add(pt)
    print(len(visited))

def f1(moves):
    ps = [(0, 0) for _ in range(10)]
    visited = set()

    for d, repeats in moves:
        direction = DIRECTIONS[d]
        for i in range(repeats):
            ps[0] = ps[0][0] + direction[0], ps[0][1] + direction[1]  # move first
            for i in range(1, 10):
                ps[i] = do_move(ps[i-1], ps[i])

            visited.add(ps[9])
    print(len(visited))
