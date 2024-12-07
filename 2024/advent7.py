def parse_line(line):
    goal, results = line.split(": ")
    goal = int(goal)
    results = [int(r) for r in results.split(" ")]
    return goal, results


def resolves(goal, results):
    length = len(results)
    operators = [' '] * length
    summed = results[:1] + [None] * (length - 1)
    index = 1
    while index > 0:
        # print(results, goal, index, summed[index])
        current_op = operators[index]
        if current_op == ' ':
            operators[index] = '+'
            summed[index] = summed[index-1] + results[index]
        elif current_op == '+':
            operators[index] = '*'
            summed[index] = summed[index-1] * results[index]
        else:
            assert current_op == '*'
            operators[index] = ' '
            index -= 1
            continue
        if index == length - 1:
            if summed[index] == goal:
                return True
        else:
            index += 1
    return False


def f1(input):
    return sum(goal for goal, results in input if resolves(goal, results))
