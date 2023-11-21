parse = lambda x: x


def f1(input):
    x, y, data = input
    step = x * y
    assert len(data) % step == 0

    part = min(
        (data[i : i + step] for i in range(0, len(data), step)),
        key=lambda x: x.count("0"),
    )
    return part.count("1") * part.count("2")
