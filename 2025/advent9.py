from shapely import Polygon, box, transform

def parse(input):
    return [tuple(map(int, line.split(","))) for line in input.split("\n")]

def f1(points):
    return max([(abs(x1-x2)+1) * (abs(y1-y2)+1) for x1, y1 in points for x2, y2 in points])

def f2(points):
    poly = Polygon(points)
    # Add right and under boundary, extend 1 block to right and bottom
    poly = poly.union(transform(poly, lambda p: p + (1, 0))).union(transform(poly, lambda p: p + (0, 1)))

    assert poly.is_valid
    def area_if_inside(p1, p2):
        min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
        min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
        bx = box(min_x, min_y, max_x+1, max_y+1)

        if poly.contains(bx):
            return bx.area
        return 0

    return int(max(area_if_inside(p1, p2) for i, p1 in enumerate(points) for p2 in points[i+1:]))
