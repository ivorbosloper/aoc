def parse_line(line):
    if not all(c in "01" for c in line):
        line = "".join("{:04b}".format(int(c, 16)) for c in line)
    return mparse(line)[1]


def mparse(line, p=0):
    version = int(line[p:p+3], 2)
    _type = int(line[p+3:p+6], 2)
    p += 6
    if _type == 4:
        bit = '1'
        v = 0
        while bit == '1':
            bit = line[p]
            val = int(line[p+1:p+5], 2)
            v = v * 16 + val
            p += 5
        return p, (version, _type, v)
    else:
        l_bit = line[p]
        p += 1
        nr_bits = 11 if l_bit == '1' else 15
        total_value = int(line[p:p+nr_bits], 2)
        p += nr_bits

        if l_bit == '0':
            original_p = p
            subs = []
            while p < original_p + total_value:
                p, t_value = mparse(line, p)
                subs.append(t_value)
            assert p == original_p + total_value
            return p, (version, _type, subs)
        else:
            subs = []
            for _ in range(total_value):
                p, t_value = mparse(line, p)
                subs.append(t_value)
            return p, (version, _type, subs)


def sum_tree(tree):
    version, _type, value = tree
    if isinstance(value, list):
        version += sum(sum_tree(sub_tree) for sub_tree in value)
    return version


def eval_tree(tree):
    from operator import mul, add, lt, gt, eq
    version, _type, value = tree
    if 0 <= _type <= 3:
        op = {0: add, 1: mul, 2: min, 3: max}[_type]
        val = eval_tree(value[0])
        for sub_tree in value[1:]:
            val = op(val, eval_tree(sub_tree))
        return val
    elif _type == 4:
        return value
    elif 5 <= _type <= 7:
        op = {5: gt, 6: lt, 7: eq}[_type]
        return 1 if op(eval_tree(value[0]), eval_tree(value[1])) else 0
    assert False


def f1(input):
    for tree in input:
        # print(tree)
        print(sum_tree(tree))


def f2(input):
    for tree in input:
        # print(tree)
        print(eval_tree(tree))



