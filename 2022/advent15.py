import re
from operator import itemgetter

def parse_line(line):
    m = re.match(r"Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)", line)
    return tuple(int(m.group(i)) for i in range(1, 5))

def get_merged_ranges_for_line(beacons, sensors, line):
    objects_on_line = len([True for x, y, dist in sensors if y == line]) \
                    + len([True for x, y in beacons if y == line])
    ranges_on_line = []
    for x, y, dist in sensors:
        ln = dist - abs(y-line)
        if ln < 0: continue
        start, end = x - ln, x + ln + 1
        ranges_on_line.append((start, end))
        # print(f"x={x}, y={y}, ln={ln}, start={start}, end={end}")
    ranges_on_line.sort(key=itemgetter(0))  # sort by start
    merged_ranges = ranges_on_line[:1]
    for rng in ranges_on_line[1:]:
        current = merged_ranges[-1]
        # if start of new range falls in current range, merge them
        if rng[0] <= current[1]:
            merged_ranges[-1] = (current[0], max(rng[1], current[1]))
        else:
            merged_ranges.append(rng)
    return objects_on_line, merged_ranges

def compose(ps):
    beacons = set()
    sensors = []
    for s in ps:
        x, y, bx, by = s
        dist = abs(x-bx) + abs(y-by)
        sensors.append((x, y, dist))
        beacons.add((bx, by))
    return beacons, sensors

def f1(ps):
    beacons, sensors = compose(ps)
    objects_on_line, merged_ranges = get_merged_ranges_for_line(beacons, sensors, line=2000000)  # or 10
    covered = sum(end-start for start, end in merged_ranges) - objects_on_line
    print(covered)

def f2(ps):
    beacons, sensors = compose(ps)
    if ps[0] == (2, 18, -2, 15):
        return
    mx = 4000000
    for line in range(mx + 1):
        objects_on_line, merged_ranges = get_merged_ranges_for_line(beacons, sensors, line=line)
        for start, end in merged_ranges:
            if 0<start<mx:
                print(line, start-1, 4000000 * (start-1) + line)
                # return  # 7146861218544
        