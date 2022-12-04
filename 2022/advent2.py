mapping = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2}

def parse_line(line):
    return [mapping[c] for c in line.split(' ')]

# Rock, Paper, Scissors

points = [1, 2, 3]
win_points = [0, 3, 6]

def score_rps(m1, m2):
    # 0 is loss, 1 is draw, 2 is winning
    # m2 is my move
    """
    0 1 == 1 win  Rock Paper
    0 2 == 2 loss Rock Sciscors
    1 0 == -1 loss Paper Rock == loss
    2 0 == -2 win Scisors Rock
    1 2 == 1 win Paper Scisscors
    2 1 == -1 loss Sciscos Paper
    # Conclusion: m2-m1 in (1, -2) == Winning
    """

    if m1 == m2:
        return 1
    return 2 if m2 - m1 in (1, -2) else 0

def f1(input):
    total = 0
    for m1, m2 in input:
        score = score_rps(m1, m2)
        total += points[m2] + win_points[score]
        # print(f"{m1},{m2} == {points[m2]} + {win_points[score]}, total {total}")
    print(total)

def f2(input):
    total = 0
    for m1, outcome in input:
        # m1 is his move
        if outcome == 0:
            m2 = (m1 - 1 + 3) %3
        elif outcome == 1:  # draw
            m2 = m1
        else:
            m2 = (m1 + 1) %3

        score = score_rps(m1, m2)
        total += points[m2] + win_points[score]
        print(f"{m1},{m2} == {points[m2]} + {win_points[score]}, total {total}")
    print(total)
