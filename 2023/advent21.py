import math
from itertools import pairwise

import numpy as np

from util import HV_VARIANTS


def shift_helper(array, shift=0, axis=0):
    # Roll the 2D array along axis with certain unity
    _array = np.roll(array, shift=shift, axis=axis)

    # Cancel the last/first slice shifted to the first/last slice
    if axis == 0:
        if shift >= 0:
            _array[:1, :] = 0
        else:
            _array[-1:, :] = 0
        return _array
    else:
        if shift >= 0:
            _array[:, :1] = 0
        else:
            _array[:, -1:] = 0
        return _array


def tostr(maze):
    pass


def f1(input):
    mask = np.asarray([[c == "#" for c in row] for row in input], dtype=bool)
    points = np.asarray([[c == "S" for c in row] for row in input], dtype=bool)

    for _ in range(64):
        points = np.where(
            mask,
            False,
            shift_helper(points, -1, 0)
            | shift_helper(points, 1, 0)
            | shift_helper(points, -1, 1)
            | shift_helper(points, 1, 1),
        )

    return np.count_nonzero(points)


def f1(input):
    mask = np.asarray([[c == "#" for c in row] for row in input], dtype=bool)
    points = np.asarray([[c == "S" for c in row] for row in input], dtype=bool)

    for _ in range(120):
        points = np.where(
            mask,
            False,
            shift_helper(points, -1, 0)
            | shift_helper(points, 1, 0)
            | shift_helper(points, -1, 1)
            | shift_helper(points, 1, 1),
        )

    return np.count_nonzero(points)


def f2(input, loop=400):
    smask = np.asarray([[c == "#" for c in row] for row in input], dtype=bool)
    point = next(
        (y, x) for y, row in enumerate(input) for x, c in enumerate(row) if c == "S"
    )
    length = max(len(input), len(input[0]))
    size = loop // (length // 2)
    size += (size + 1) % 2
    mask = np.tile(smask, (size, size))
    points = np.zeros(mask.shape, dtype=bool)
    points[(size // 2) * smask.shape[0] + point[0]][
        (size // 2) * smask.shape[1] + point[1]
    ] = True
    results = [1]
    for _ in range(loop):
        points = np.where(
            mask,
            False,
            shift_helper(points, -1, 0)
            | shift_helper(points, 1, 0)
            | shift_helper(points, -1, 1)
            | shift_helper(points, 1, 1),
        )
        results.append(np.count_nonzero(points))

    # print(results)
    # print([b - a for a, b in pairwise(results)])
    # print([b - a for a, b in pairwise([v for i, v in enumerate(results) if v % 2])])
    # 26501365 == 5 x 11 x 481843
    # for a, b in pairwise(results):
    #     print(b / a)
    modulo = 26501365 % smask.shape[0]
    # after modulo, it expands

    m = results[modulo + smask.shape[0]] - results[modulo]
    n = results[modulo + smask.shape[0] * 2] - results[modulo + smask.shape[0]]
    a = (n - m) // 2
    b = m - 3 * a
    c = results[modulo] - b - a

    ceiling = math.ceil(26501365 / smask.shape[0])
    # 616951894542012 too high, one step off... Begin results with [1]
    # 616951804315987

    return a * ceiling**2 + b * ceiling + c
