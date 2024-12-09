from llist import dllist as mlist # see https://ajakubek.github.io/python-llist/index.html
import itertools

def pr(fs):
    print(fs)
    print("".join([(chr(48 + c) if c is not None else ".") * i for c, i in fs]))


def f1(input):
    fs = mlist([[i//2 if (i % 2 == 0) else None, int(c)] for i, c in enumerate(input[0]) if c != '0'])

    def next_empty(node):
        while node is not None and node.value[0] is not None:
            node = node.next
        return node

    left = next_empty(fs.first)
    while left is not None:
        right = fs.last
        empty, space = left.value
        fid, length = right.value

        # print(left, right)
        # pr(fs)

        # Invariant
        assert empty is None
        assert space and length
        assert left != right

        to_move = min(space, length)
        # print("to_move", to_move, left, right)

        left.value[0] = fid
        left.value[1] = to_move
        right.value[1] -= to_move

        if space > to_move:
            # print("insertafter", space-to_move)
            left = fs.insertafter([None, space-to_move], left)
        else:
            left = next_empty(left)
        while right.value[0] is None or right.value[1] == 0:
            right = right.prev
            fs.pop()
            if right == left:
                left = None

    lst = list(itertools.chain.from_iterable([c for i in range(length)] for c, length in fs))
    return sum(i * c for i, c in enumerate(lst))


def f2(input):
    fs = mlist([[i//2 if (i % 2 == 0) else None, int(c)] for i, c in enumerate(input[0]) if c != '0'])

    right = fs.last
    while right is not None:
        fid, length = right.value

        # Invariant
        assert fid is not None
        assert length

        left = fs.first
        while left is not None:
            if left == right:
                left = None
                break
            if left.value[0] is None and left.value[1] >= length:
                break
            left = left.next

        if left:
            space = left.value[1] - length
            left.value[0] = fid
            left.value[1] = length
            if space > 0:
                fs.insertafter([None, space], left)
            right.value[0] = None
            for adjacent in (right.next, right.prev):
                if adjacent and adjacent.value[0] is None:
                    right.value[1] += adjacent.value[1]
                    fs.remove(adjacent)

        if right is not None:
            right = right.prev
            if right and right.value[0] is None:
                right = right.prev

        if right is not None:
            assert right.value[0] is not None

    lst = list(itertools.chain.from_iterable([c for i in range(length)] for c, length in fs))
    return sum(i * c for i, c in enumerate(lst) if c is not None)
