def parse_line(l):
    def value_color(s):
        ss = s.split(' ')
        return {"count": int(ss[0]), "color": ' '.join(ss[1:-1])}

    color, groups = l[:-1].split(' bags contain ')
    return color, [value_color(s) for s in groups.split(', ') if not s.startswith('no ')]


def build_graphs(input):
    nodes, reverse = {}, {}  # {color -> node: {color: color, links: [{node, count}]}
    for color, links in input:
        nodes[color] = {"color": color, "links": links}
        reverse.setdefault(color, {"color": color, "links": []})
        for l in links:
            nodes.setdefault(l["color"], {"color": l["color"], "links": []})
            reverse.setdefault(l["color"], {"color": l["color"], "links": []})['links'].append(color)
    return nodes, reverse


def f1(input):
    nodes, reverse = build_graphs(input)
    queue = ['shiny gold']
    reached = set()
    first = True
    while len(queue):
        color = queue.pop()
        if color in reached:
            continue
        if first:
            first = False
        else:
            reached.add(color)
        queue.extend(reverse[color]['links'])
    return len(reached)


def f2(input):
    nodes, reverse = build_graphs(input)
    cache = {}

    def calculate_contained_bags(color):
        print(color)
        if color in cache:
            return cache[color]
        value = sum(c['count'] * (calculate_contained_bags(c['color'])+1) for c in nodes[color]['links'])
        cache[color] = value
        return value

    return calculate_contained_bags('shiny gold')
