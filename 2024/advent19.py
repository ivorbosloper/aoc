def parse(inp):
    lines = inp.splitlines()
    return lines[0].split(", "), lines[2:]


def f1(inp):
    patterns, designs = inp

    def can_make(design):
        for p in patterns:
            if design == p:
                return True
            if design.startswith(p):
                if can_make(design[len(p):]):
                    return True
        return False

    return sum(can_make(design) for design in designs)


def f2(inp):
    patterns, designs = inp
    patterns = set(patterns)
    lengths = {len(p) for p in patterns}

    def count(design):
        # Take a piece of the beginning, calculate the ways, multiply by rest
        # e.g., generate all triples of patterns a+b+c for each of the patterns
        # production that's 447*447*447 == 89M :(. NO.

        # Or, use a TRIE (prefix tree) where you realize... hmm. NO

        # Or, create a state-machine that's matching multiple things at the same time.... NO.

        # Or, build up a memoized 'cache' of ways to get from start to point to here
        # For each point, see if you up-till-here can eat out a piece (for each length of patterns)
        # And add the possibilities of the (possibilites[part-before-piece-of-cake-out])
        # to the possibilities[up-till-here]

        possibilities = [1] + [0 for _ in design]
        for i in range(1, len(design) + 1):
            for cut in lengths:
                if i < cut:
                    continue  # can not eat such large piece
                piece = design[i - cut:i]
                if piece in patterns:
                    possibilities[i] += possibilities[i - cut]
        return possibilities[-1]

    return sum(count(design) for design in designs)
