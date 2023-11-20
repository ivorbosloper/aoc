import re


def parse_line(line):
    m = re.match(r"^([\w ]+) \(contains (.*)\)$", line)
    return m.group(1).split(" "), m.group(2).split(", ")


class Graph:
    def __init__(self, input) -> None:
        self.ingredients = []
        self.allergens = []

        for coded, decoded in input:
            self.ingredients.append(set(coded))
            self.allergens.append(set(decoded))

        self.distinct_ingredients = set()
        self.distinct_ingredients.update(*self.ingredients)
        self.distinct_allergens = set()
        self.distinct_allergens.update(*self.allergens)

    def count(self, ingredient):
        return sum(ingredient in ing for ing in self.ingredients)

    def options(self, allergen):
        return set.intersection(
            *[
                ingredients
                for ingredients, allergens in zip(self.ingredients, self.allergens)
                if allergen in allergens
            ]
        )

    def resolve(self):
        ingredient_to_allergen = {}
        while len(ingredient_to_allergen) < len(self.distinct_allergens):
            for a in self.distinct_allergens:
                if a in ingredient_to_allergen:
                    continue

                options = self.options(a).difference(ingredient_to_allergen)
                if len(options) == 1:
                    ingredient_to_allergen[options.pop()] = a
        return ingredient_to_allergen


def f1(input):
    graph = Graph(input)
    ingredient_to_allergen = graph.resolve()

    return sum(
        graph.count(a)
        for a in graph.distinct_ingredients.difference(ingredient_to_allergen)
    )


def f2(input):
    graph = Graph(input)
    ingredient_to_allergen = graph.resolve()
    inverted = {v: k for k, v in ingredient_to_allergen.items()}

    return ",".join([inverted[a] for a in sorted(ingredient_to_allergen.values())])
