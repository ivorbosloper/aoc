#!/usr/bin/env python3

import sys
import importlib
from io import StringIO

USAGE = "run <year> <day>"


def apply_parse(input, func):
    return [func(s.strip()) for s in StringIO(input)]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)
    year, day = int(sys.argv[1]), int(sys.argv[2])
    assert 2015 <= year <= 2025
    assert 0 < day < 30

    m = importlib.import_module(f'{year}.advent{day}')
    test_data, prod_data = getattr(importlib.import_module(f'{year}.data'), f'a{day}')

    func = getattr(m, 'parse', None)
    if func:
        test_data, prod_data = func(test_data), func(prod_data)
    else:
        func = getattr(m, 'parse_line', lambda x: x)
        test_data, prod_data = apply_parse(test_data, func), apply_parse(prod_data, func)

    for func_name in ('f', 'f1', 'f2'):
        if hasattr(m, func_name):
            func = getattr(m, func_name)
            print(f"- {func_name:4}-")
            sys.stdout.write('test> '); sys.stdout.flush(); func(test_data)
            sys.stdout.write('prod> '); sys.stdout.flush(); func(prod_data)
