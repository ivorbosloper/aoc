from operator import mul, add


def parse_line(line):
    goal, results = line.split(": ")
    goal = int(goal)
    results = [int(r) for r in results.split(" ")]
    return goal, results


def resolves(goal, results, ops=(None, add, mul)):
    length = len(results)
    operators = [None] * length
    summed = results[:1] + [None] * (length - 1)
    index = 1
    while index > 0:
        # print(results, goal, index, summed[index])
        current_op = operators[index]
        if current_op == ops[-1]:
            operators[index] = None
            index -= 1
            continue

        op_index = ops.index(current_op)
        current_op = operators[index] = ops[op_index+1]
        summed[index] = current_op(summed[index - 1], results[index])

        if index == length - 1:
            if summed[index] == goal:
                return True
        else:
            index += 1
    return False


def f1(input):
    return sum(goal for goal, results in input if resolves(goal, results))


def concat(n1, n2):
    return int(str(n1) + str(n2))


def f2(input):
    ops = (None, add, mul, concat)
    return sum(goal for goal, results in input if resolves(goal, results, ops=ops))
