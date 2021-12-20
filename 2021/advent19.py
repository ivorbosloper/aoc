def transformations(x, y, z):
    return [f for vectors in [((x2, y2, z2), (-y2, x2, z2), (-x2, -y2, z2), (y2, -x2, z2)) for (x2, y2, z2) in (
            (x, y, z), (x, z, -y), (x, -y, -z), (x, -z, y), (-z, y, x), (z, y, -x))] for f in vectors]


class Scanner:
    def __init__(self, coords):
        self.transformed = [[] for _ in range(24)]
        for point in coords:
            for p, pos in enumerate(transformations(*point)):
                self.transformed[p].append(pos)
        self.fixed = None
        self.pos = None  # towards scanner[0]

    def init(self):
        self.fixed = set(self.transformed[0])
        self.pos = (0, 0, 0)

    def try_pair(self, scanners):
        if not self.fixed:
            for scanner in scanners:
                if scanner.fixed and self.find_overlap(scanner):
                    return

    def find_overlap(self, s2):
        for t_vectors in self.transformed:
            for x2, y2, z2 in s2.fixed:
                for x1, y1, z1 in t_vectors:
                    transformed = {(x + x2 - x1, y + y2 - y1, z + z2 - z1) for x, y, z in t_vectors}
                    overlap = transformed & s2.fixed
                    if len(overlap) >= 12:
                        self.fixed = transformed
                        self.pos = (x2 - x1, y2 - y1, z2 - z1)
                        return True


def parse_scanners(input):
    coords = None
    scanners = []
    for line in input:
        if not line: continue
        if line.startswith('---'):
            if coords:
                scanners.append(Scanner(coords))
            coords = []
            continue
        coords.append([int(i) for i in line.split(',')])
    scanners.append(Scanner(coords))
    return scanners


def f1(input):
    scanners = parse_scanners(input)
    scanners[0].init()

    while not all(s.fixed for s in scanners):
        print(f"Searching for {len([s for s in scanners if not s.fixed])}")
        for scanner in scanners:
            scanner.try_pair(scanners)

    beacons = set(f for scanner in scanners for f in scanner.fixed)

    m = 0
    for s1 in scanners:
        for s2 in scanners:
            if s1 != s2:
                m = max(m, sum(abs(s1.pos[i] - s2.pos[i]) for i in range(3)))

    print("Max: ", m)
    return len(beacons)
