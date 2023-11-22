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


def f2(input):
    x, y, data = input
    step = x * y
    assert len(data) % step == 0

    # 0 black, 1 white, 2 transparent
    result = list(data[0:step])
    for base in range(step, len(data), step):
        for i in range(step):
            if result[i] == "2":
                result[i] = data[base + i]

    print()
    result = "".join(result).replace("0", " ")
    return "\n".join([result[i * x : i * x + x] for i in range(y)])
