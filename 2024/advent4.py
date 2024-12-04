import re

regex = re.compile('XMAS')
rregex = re.compile('SAMX')


def diagonalize(matrix):
    y_size, x_size = len(matrix), len(matrix[0])
    return [''.join(matrix[x - i][i] for i in range(min(x + 1, x_size))) for x in range(y_size)] \
         + [''.join(matrix[y_size - 1 - i][i + y] for i in range(min(x_size - y, y_size))) for y in range(1, x_size)]


def f1(input):
    def count(*matrices):
        return sum(len(regex.findall(m)) + len(rregex.findall(m)) for m in map("\n".join, matrices))

    transposed = [''.join(b[::-1]) for b in zip(*input)]
    return count(input, transposed, diagonalize(input), diagonalize(transposed))


def f2(matrix):
    y_size, x_size = len(matrix), len(matrix[0])
    def is_ms(a, b):
        return a in 'MS' and b in 'MS' and a != b

    return sum(matrix[y][x] == 'A'
               and is_ms(matrix[y-1][x-1], matrix[y+1][x+1])
               and is_ms(matrix[y-1][x+1], matrix[y+1][x-1])
               for x in range(1, x_size-1) for y in range(y_size-1))
