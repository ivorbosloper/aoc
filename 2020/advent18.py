import operator
from functools import reduce

from pyparsing import ParserElement, Suppress, Forward, Group, ZeroOrMore, oneOf, OpAssoc, infix_notation
from pyparsing.common import pyparsing_common

ParserElement.enable_left_recursion()
op_map = {
    "+": operator.add,
    "*": operator.mul
}


def my_eval(expr):  # evaluate left to right
    if isinstance(expr, int):
        return expr
    result = my_eval(expr[0])
    for i in range(1, len(expr), 2):
        op, operand = op_map[expr[i]], my_eval(expr[i+1])
        result = op(result, operand)
    return result


def f1(input):
    lpar, rpar = map(Suppress, '()')
    expr = Forward()
    factor = pyparsing_common.integer | Group(lpar + expr + rpar)
    expr <<= factor + ZeroOrMore(oneOf('+ *') + factor)

    result = [my_eval(expr.parse_string(line)) for line in input]
    return reduce(operator.add, result)


def f2(input):
    expr = infix_notation(pyparsing_common.integer, [
            ('-', 1, OpAssoc.RIGHT),
            (oneOf('+'), 2, OpAssoc.LEFT),
            (oneOf('*'), 2, OpAssoc.LEFT),
    ])

    result = [my_eval(expr.parse_string(line)) for line in input]
    return reduce(operator.add, result)
