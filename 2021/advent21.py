from collections import defaultdict


def parse(input):
    return input


def f1(input):
    score1, score2 = 0, 0
    pos1, pos2 = input
    pos1 -= 1
    pos2 -= 1
    rolls = 0

    def roll():
        die = 0
        while True:
            yield die + 1
            die = (die + 1) % 1000

    r = roll()

    while score2 < 1000:
        pos1 = (pos1 + next(r) + next(r) + next(r)) % 10
        score1 += pos1+1
        rolls += 3
        if score1 >= 1000:
            break
        pos2 = (pos2 + next(r) + next(r) + next(r)) % 10
        score2 += pos2 + 1
        rolls += 3
        # print("pos", pos1+1, pos2+2, "scores", score1, score2)

    # print("score", score1, score2, "rolls", rolls)
    return min(score1, score2) * rolls


def f2(input):
    nrs = defaultdict(int)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                nrs[i+j+k+3] += 1

    states = {(input[0]-1, input[1]-1, 0, 0): 1}  # (pos1, pos2, score1, score2) -> nr_of_occurrences
    winning = defaultdict(int)
    turn = 0
    while len(states):
        n_states = defaultdict(int)
        for s, s_times in states.items():
            pos1, pos2, score1, score2 = s
            if score1 >= 21 or score2 >= 21:
                # check for winning states, move them in winning-universe
                winning[s] += s_times
                continue
            for roll, nr in nrs.items():
                if turn % 2 == 0:
                    npos = (pos1+roll) % 10
                    key = (npos, pos2, score1+npos+1, score2)
                else:
                    npos = (pos2 + roll) % 10
                    key = (pos1, npos, score1, score2 + npos + 1)

                n_states[key] += s_times * nr

        turn += 1
        states = n_states

    s1, s2 = (sum(s_times for s, s_times in winning.items() if s[i] >= 21) for i in range(2, 4))
    return max(s1, s2)
