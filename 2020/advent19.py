import operator
import re
import tatsu
from collections import defaultdict
from functools import reduce
from pyparsing import Literal, Forward


def parse(input):
    return [block.split("\n") for block in input.split("\n\n")]


def f1(blocks):
    rules, messages = blocks
    expressions = defaultdict(Forward)

    for r in rules:
        nr, rest = r.split(": ")
        if rest.startswith('"'):
            expr = Literal(eval(rest))
        else:
            expr = reduce(operator.__or__,
                          ((reduce(operator.add, (
                                 (expressions[factor] for factor in term.split(" ")))))
                           for term in rest.split(" | ")))
        if nr in expressions:
            expressions[nr] <<= expr
        else:
            expressions[nr] = expr
    return len([m for m in messages if expressions["0"].matches(m)])


def f2(blocks):
    rules, messages = blocks

    new_rules = ["8: 42 | 42 8" if rule.startswith('8:') else
                 "11: 42 31 | 42 11 31" if rule.startswith('11:') else rule for rule in rules]

    # return f1([new_rules, messages])

    grammar = "@@grammar::F2\nstart = expression0 $ ;\n"
    for r in new_rules:
        nr, rest = r.split(": ")
        if rest.startswith('"'):
            expr = rest.replace('"', "'")
        else:
            expr = re.sub(r'(\d+)', r'expression\1', rest)
        grammar += f"expression{nr} = {expr} ;\n"

    # print(grammar)
    model = tatsu.compile(grammar)
    valids = 0
    for m in messages:
        try:
            model.parse(" ".join(m))
            valids += 1
        except:
            pass
    return valids