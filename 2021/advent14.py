from collections import defaultdict


def replace(template, replacements):
    return "".join(c + replacements[c + template[i+1]] if c + template[i+1] in replacements else c
                   for i, c in enumerate(template[:-1])) + template[-1]


def cnt(template):
    d = {}; [d.update({c: d.get(c, 0) + 1}) for c in template]
    return d


def f1(input):
    template = input[0]
    replacements = dict(a.split(" -> ") for a in input[2:])

    for _ in range(10):
        template = replace(template, replacements)
    d = cnt(template)

    vals = sorted(d.values())
    return vals[-1] - vals[0]


def f2(input):
    template = input[0]
    replacements = dict(a.split(" -> ") for a in input[2:])
    replace_pairs = {k: (k[0]+v, v+k[1]) for k, v in replacements.items()}
    pair_count = cnt(template[i:i+2] for i in range(len(template) -1))
    for _ in range(40):
        new_pair_count = defaultdict(int)
        for pair, count in pair_count.items():
            if len(pair) > 1:
                for p in replace_pairs.get(pair, [pair[0]]):
                    new_pair_count[p] += count
        pair_count = new_pair_count

    d = defaultdict(int)
    d[template[-1]] = 1
    for pair, count in pair_count.items():
        d[pair[0]] += count

    # print(d)
    vals = sorted(d.values())
    return vals[-1] - vals[0]
