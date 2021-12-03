from io import StringIO

DIRS = dict(
    down=[0, 1],
    up=[0, -1],
    forward=[1, 0],
)


def f1(data):
    state = 0, 0
    for i in StringIO(data):
        direction, nr = i.strip().split(" ")
        move = DIRS[direction]
        state = state[0] + move[0] * int(nr), state[1] + move[1] * int(nr)
    return state[0] * state[1]
