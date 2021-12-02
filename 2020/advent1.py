parse_line = int


def f1(data):
    for i, v1 in enumerate(data):
        for v2 in data[i+1:]:
            if v1 + v2 == 2020:
                print(v1*v2)


def f2(data):
    for i, v1 in enumerate(data):
        for j, v2 in enumerate(data[i+1:]):
            for v3 in data[j + 1:]:
                if v1 + v2 + v3 == 2020:
                    print(v1*v2*v3)
