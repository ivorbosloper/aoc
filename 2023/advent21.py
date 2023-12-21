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
    zeros = np.zeros(points.shape, dtype=bool)

    for _ in range(200):
        # print()
        # print("\n".join(["".join(["O" if x else "." for x in row]) for row in points]))
        points = np.where(
            mask,
            zeros,
            shift_helper(points, -1, 0)
            | shift_helper(points, 1, 0)
            | shift_helper(points, -1, 1)
            | shift_helper(points, 1, 1),
        )

    return np.count_nonzero(points)
