import re
import itertools
import collections

def parse_line(line):
    m = re.match("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. "
                 "Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore "
                 "and (\d+) obsidian.", line)
    return tuple(int(i) for i in m.groups())


def add(p1, p2):
    return tuple(i+j for i, j in zip(p1, p2))

def sme(p1, p2):  # smaller or equal
    return all(e1 <= e2 for e1, e2 in zip(p1, p2))

def cmp(p1, p2):  # -1 if smaller, 0 if undecided, 1 if larger
    diff = (e1 - e2 for e1, e2 in zip(p1, p2))
    return -1 if all(e <= 0 for e in diff) else 1 if all(e >= 0 for e in diff) else 0

ORE, CLAY, OBSIDIAN, GEODE = range(4)

SKIP = (0,)
TRY_BOTH = (0, 1)

def calc(blueprints, cycles=24):
    blueprint_scores = {}
    stop_at_cycle = {cycles-16: ORE, cycles-7: CLAY, cycles-4: OBSIDIAN}

    for blueprint in blueprints:
        blueprint_nr, ore_robot_ore, clay_robot_ore, obsidian_robot_ore, obsidian_robot_clay, \
            geode_robot_ore, geode_robot_obsidian = blueprint

        max_useful = [ore_robot_ore + clay_robot_ore + obsidian_robot_ore + geode_robot_ore,
                      obsidian_robot_clay, geode_robot_obsidian, 100000]

        def options(robots, stock):
            should_build = ( # if you can build anything, you have to build something
                stock[ORE] >= ore_robot_ore and
                stock[ORE] >= clay_robot_ore and  # can build max x clay robots
                stock[ORE] >= obsidian_robot_ore and stock[CLAY] >= obsidian_robot_clay and
                stock[ORE] >= geode_robot_ore and stock[OBSIDIAN] >= geode_robot_obsidian
            )

            for r1 in TRY_BOTH if stock[ORE] >= ore_robot_ore and robots[ORE] < max_useful[ORE] else SKIP:
                ore_1 = stock[ORE] - r1 * ore_robot_ore
                for r2 in TRY_BOTH if ore_1 >= clay_robot_ore and robots[CLAY] < max_useful[CLAY] else SKIP:
                    ore_2 = ore_1 - clay_robot_ore * r2
                    for r3 in TRY_BOTH if ore_2 >= obsidian_robot_ore \
                                    and stock[CLAY] >= obsidian_robot_clay \
                                    and robots[OBSIDIAN] < max_useful[OBSIDIAN] else SKIP:
                        ore_3 = ore_2 - obsidian_robot_ore * r3
                        clay_3 = stock[CLAY] - obsidian_robot_clay * r3
                        # ALWAYS BUILD GEODE bot if possible
                        r4 = 1 if ore_3 >= geode_robot_ore and stock[OBSIDIAN] >= geode_robot_obsidian else 0
                        if should_build and r1 == r2 == r3 == r4 == 0:
                            continue
                        ore_4 = ore_3 - geode_robot_ore * r4
                        obsidian_4 = stock[OBSIDIAN] - geode_robot_obsidian * r4
                        yield (
                            (robots[ORE] + r1, robots[CLAY] + r2, robots[OBSIDIAN] + r3, robots[GEODE] + r4),
                            (ore_4 + robots[ORE], clay_3 + robots[CLAY], obsidian_4 + robots[OBSIDIAN], stock[GEODE] + robots[GEODE])
                        )

        # Robots : (ore, clay, obsidian, geode) -->{Stock[ore, clay, obsidian, geode]}
        states = {(1, 0, 0, 0): {(0, 0, 0, 0)}}
        robot_seen = collections.defaultdict(set)   # -> dict((r1, r2, r3, r4) --> [(m1, m2, m3, m4)])

        for cycle in range(cycles):
            new_states = collections.defaultdict(set)
            remove = set()
            for r, ss in states.items():
                for s in ss:
                    for robots, stock in options(r, s):
                        my_group = robot_seen[robots]
                        if stock in my_group:
                            continue
                        for seen in my_group:
                            diff = cmp(stock, seen)
                            if diff > 0:  # element is larger than comparison, remove small stuff
                                remove.add(seen)
                            elif diff < 0:  # element to be added is too small
                                stock = None
                                break
                            # >= continue searching
                        while len(remove):
                            my_group.remove(remove.pop())
                        if stock:
                            my_group.add(stock)
                            new_states[robots].add(stock)

            max_r = tuple(max(r[i] for r in new_states) for i in range(4))
            geode_diff = 2
            if max_r[GEODE]:
                geode_diff = 1

            if cycle in stop_at_cycle:
                max_useful[stop_at_cycle[cycle]] = 0

            to_remove = [r for r in new_states if r[GEODE] <= max_r[GEODE] - geode_diff]
            for r in to_remove:
                del robot_seen[r]
                del new_states[r]

            # print(cycle, len(states), len(new_states), sum(len(ss) for ss in new_states.values()))
            states = new_states
        blueprint_scores[blueprint_nr] = max(stock[GEODE] for stocks in states.values() for stock in stocks)        
    return blueprint_scores

def f1(blueprints):
    blueprint_scores = calc(blueprints)
    print(blueprint_scores)
    return sum(nr * mx for nr, mx in blueprint_scores.items())


def f2(blueprints):
    blueprint_scores = calc(blueprints[:3], cycles=24)
    print(blueprint_scores)
    return blueprint_scores[1] * blueprint_scores[2] * blueprint_scores[3]
