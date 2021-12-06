def parse(input):
    return [int(i) for i in input.split(",")]


def simulate(input, days):
    population = [0 for _ in range(9)]
    for i in input:
        population[i] += 1

    for day in range(days):
        head, *new_population = population
        new_population[6] += head
        new_population.append(head)
        population = new_population

    print(sum(population))


def f1(input):
    simulate(input, 80)


def f2(input):
    simulate(input, 256)
