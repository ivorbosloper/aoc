parse_line = int

cache = {}


def composed_fuel(mass):
    if mass < 9:
        return 0
    if mass in cache:
        return cache[mass]
    fuel = mass // 3 - 2
    fuel += composed_fuel(fuel)
    cache[mass] = fuel
    return fuel


def f1(input):
    return sum(mass // 3 - 2 for mass in input)


def f2(input):
    return sum(composed_fuel(mass) for mass in input)
