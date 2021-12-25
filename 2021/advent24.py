# class Node:
#     def __init__(self, prefix, vars):
#         self.prefix = 0
#         self.vars = [0, 0, 0, 0]  # w, x, y, z
import operator
import sys

MAP = {'add': '+', 'mul': '*', 'div': '//', 'mod': '%'}


def parse_program(input, next_var=None):
    assert input[0].startswith('inp ')
    program = []
    for line in input:
        cmd, *args = line.split(" ")
        if cmd == 'inp':
            program.append(f"def f(key, {args[0]}):")
            statement = f"{', '.join(c for c in 'wxyz' if c != args[0])} = key"
        elif cmd == 'eql':
            statement = f"{args[0]} = int({args[0]}=={args[1]})"
        else:
            statement = f"{args[0]} {MAP[cmd]}= {args[1]}"
        program.append("  " + statement)

    if next_var:
        program.append(f"  return {', '.join(c for c in 'wxyz' if c != next_var)}")
    else:
        program.append(f"  return z == 0")  # last program, only interested in z==0
    print("\n".join(program))
    res = {}
    exec(compile("\n".join(program), "", "exec"), None, res)
    return res['f']


def f1(input, compare_operator=operator.gt):
    if compare_operator == operator.gt: return
    default_highest = 0 if compare_operator == operator.gt else sys.maxsize
    programs, todo = [], []
    for line in input:
        if line.startswith('inp '):
            if len(todo):
                programs.append(parse_program(todo, line.split(' ')[-1]))
            todo = []
        todo.append(line)
    programs.append(parse_program(todo))

    import timeit
    starttime = timeit.default_timer()

    result = {(0, 0, 0): 0}  # v1, v2, v3 --> highest prefix
    for i in range(len(programs)):
        print(f"i={i} len={len(result)} {timeit.default_timer() - starttime:0.4f} seconds")
        starttime = timeit.default_timer()
        func = programs[i]
        runover = result
        result = {}
        for base, highest in runover.items():
            for input_nr in range(1, 10):
                key = func(base, input_nr)
                prefix = highest * 10 + input_nr
                if compare_operator(prefix, result.get(key, default_highest)):
                    result[key] = prefix
    return result.get(True) or result


def f2(input):
    f1(input, operator.lt)
