from collections import defaultdict


def f1(input):
    beams = {input[0].index("S")}
    width = len(input[0])
    splits = 0
    for line in input[1:]:
        new_beams = set()
        for beam in beams:
            if line[beam] == ".":
                new_beams.add(beam)
            else:
                assert line[beam] == "^"
                splits += 1
                if beam > 0:
                    new_beams.add(beam - 1)
                if beam < width - 1:
                    new_beams.add(beam + 1)
        beams = new_beams
        # print("".join("|" if x in beams else e for x, e in enumerate(line) ))

    return splits

def f1(input):
    beams = {input[0].index("S"): 1}
    width = len(input[0])
    for line in input[1:]:
        new_beams = defaultdict(int)
        for beam, value in beams.items():
            if line[beam] == ".":
                new_beams[beam] += value
            else:
                assert line[beam] == "^"
                if beam > 0:
                    new_beams[beam - 1] += value
                if beam < width - 1:
                    new_beams[beam + 1] += value
        beams = new_beams
        # print("".join("|" if x in beams else e for x, e in enumerate(line) ))

    return sum(beams.values())
