from functools import reduce


OPS = [(y, x) for y in range(-1, 2) for x in range(-1, 2)]


def times_two_plus(x, y):
    return x*2 + y


class Image:
    def __init__(self, input):
        self.bitmask = [c == '#' for c in input[0]]
        self.image = [[c == '#' for c in line] for line in input[2:]]
        self.background = False
        self.height = len(self.image)
        self.width = len(self.image[0])

    def new_value(self, y, x):
        index = reduce(times_two_plus,
                       (self.image[y+dy][x+dx] if 0 <= x+dx < self.width and 0 <= y+dy < self.height else self.background
                        for dy, dx in OPS))
        return self.bitmask[index]

    def scale(self):
        self.image = [[self.new_value(y, x) for x in range(-1, self.width+1)] for y in range(-1, self.height+1)]
        self.background = self.bitmask[511 if self.background else 0]
        self.width += 2
        self.height += 2

    def count(self):
        return sum(e for line in self.image for e in line)

    def __str__(self):
        return "\n".join("".join('#' if e else "." for e in row) for row in self.image)


def f1(input):
    image = Image(input)
    image.scale()
    image.scale()
    return image.count()


def f2(input):
    image = Image(input)
    for i in range(50):
        image.scale()
    return image.count()
