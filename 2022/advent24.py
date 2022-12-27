from io import StringIO
from collections import deque
import math

HV_VARIANTS = ((1, 0), (0, 1),  (-1, 0), (0, -1))
HV_MAP = dict(zip(">v<^", HV_VARIANTS))

HV_VARIANTS_OR_WAIT = HV_VARIANTS + ((0,0),)


class Maze(object):
    def __init__(self, input) -> None:
        self.blizzards = []
        for y, line in enumerate(StringIO(input)):
            for x, c in enumerate(line):
                if c in HV_MAP:
                    self.blizzards.append((x-1, y-1, c))
        self.width, self.height =  x-1, y -1
        self.modulo = math.lcm(self.width, self.height)
        self.maze_for_cycle = {}
        self.start = (0, -1)
        self.end = (self.width-1, self.height)


    def get_maze_for_cycle(self, cycle):
        xc = cycle % self.width
        yc = cycle % self.height
        maze = self.maze_for_cycle.get((xc, yc))
        if not maze:
            maze = [[0] * self.width for _ in range(self.height)]
            for (bx, by, c) in self.blizzards:
                direction = HV_MAP[c]
                if direction[0]:
                    bx = (bx + direction[0] * xc + self.width) % self.width
                else:
                    by = (by + direction[1] * yc + self.height) % self.height
                maze[by][bx] += 1
            self.maze_for_cycle[(xc, yc)] = maze
        return maze

    def shortest_path(self, start, end, cycle=0):
        queue = deque([(cycle, start)])
        seen = set()

        while len(queue):
            cycle, p = queue.popleft()
            new_e = (cycle % self.modulo, p)
            if new_e in seen:
                continue
            seen.add(new_e)
            maze = self.get_maze_for_cycle((cycle+1) % self.modulo)
            for dir in HV_VARIANTS_OR_WAIT:
                pos = p[0] + dir[0], p[1] + dir[1]
                if pos == end:
                    return cycle+1
                if pos == start or (0 <= pos[0] < self.width and 0 <= pos[1] < self.height and maze[pos[1]][pos[0]] == 0):
                    queue.append((cycle+1, pos))
        

def parse(input):
    return Maze(input)


def f1(maze):
    return maze.shortest_path(maze.start, maze.end)

def f2(maze):
    c1 = maze.shortest_path(maze.start, maze.end)
    c2 = maze.shortest_path(maze.end, maze.start, c1+1)
    return maze.shortest_path(maze.start, maze.end, c2+1)
