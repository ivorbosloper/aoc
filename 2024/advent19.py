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
