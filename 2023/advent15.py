import re


def parse(input):
    return input.split(",")


def hash(s):
    result = 0
    for c in s:
        result = ((result + ord(c)) * 17) % 256
    return result


def f1(input):
    return sum(hash(i) for i in input)


def f2(input):
    boxes = [{} for _ in range(256)]
    for s in input:
        assert (m := re.match(r"(\w+)([=-])(\d*)", s))
        label, sign, focal = m.groups()
        box = boxes[hash(label)]
        if sign == "-":
            box.pop(label, None)
        elif sign == "=":
            box[label] = int(focal)
        else:
            raise
        # print()
        # print(f"After '{s}':")
        # for i in range(256):
        #     if boxes[i]:
        #         a = " ".join(f"[{k} {v}]" for k, v in boxes[i].items())
        #         print(f"Box {i}: {a}")

    return sum(
        (1 + i) * (k + 1) * v
        for i in range(256)
        for k, v in enumerate(boxes[i].values())
    )
