from copy import deepcopy


class Node:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value  # either a number or a []

    @property
    def is_leaf(self):
        return isinstance(self.value, int)

    def __str__(self):
        if self.is_leaf:
            return str(self.value)
        return f"[" + ",".join(str(v) for v in self.value) + "]"

    @property
    def left(self):
        return self.value[0]

    @property
    def right(self):
        return self.value[1]

    def explode(self, depth=0):
        if self.is_leaf:
            return False

        if depth >= 4 and self.left.is_leaf and self.right.is_leaf:
            left = self.sibling_leaf()
            if left:
                left.value += self.left.value
            right = self.sibling_leaf(1)
            if right:
                right.value += self.right.value
            self.value = 0
            return True
        return self.left.explode(depth+1) or self.right.explode(depth+1)

    def split(self):
        if self.is_leaf:
            if self.value >= 10:
                left_val = self.value // 2
                self.value = [Node(self, left_val), Node(self, self.value - left_val)]
                return True
        else:
            return self.left.split() or self.right.split()

    def reduce(self):
        return self.explode() or self.split()

    def reduced(self):
        while self.reduce():
            pass
        return self

    def sibling_leaf(self, direction=0):  # 0 == left, 1 = right
        if self.parent:
            assert not self.parent.is_leaf
            p = self.parent.value[direction]
            if self == p:
                return self.parent.sibling_leaf(direction)  # still go up

            # I'm the opposite leaf. Go down on the other sibling
            direction = 0 if direction == 1 else 1
            while not p.is_leaf:
                p = p.value[direction]
            return p

    @property
    def magnitude(self):
        return self.value if self.is_leaf else self.value[0].magnitude * 3 + self.value[1].magnitude * 2


def parse_tree(value, parent=None):
    if isinstance(value, int):
        return Node(parent, value)
    assert isinstance(value, list)
    n = Node(parent, None)
    n.value = [parse_tree(v, parent=n) for v in value]
    return n


def f1(input):
    # assert parse_tree([[1,2],[[3,4],5]]).magnitude == 143
    # assert parse_tree([[[[0,7],4],[[7,8],[6,0]]],[8,1]]).magnitude == 1384
    # assert parse_tree([[[[1,1],[2,2]],[3,3]],[4,4]]).magnitude == 445
    # assert parse_tree([[[[3,0],[5,3]],[4,4]],[5,5]]).magnitude == 791
    # assert parse_tree([[[[5,0],[7,4]],[5,5]],[6,6]]).magnitude == 1137
    # assert parse_tree([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]).magnitude == 3488
    input = [parse_tree(eval(line)) for line in input]
    tree = input[0]
    for t2 in input[1:]:
        t1 = tree
        tree = Node(None, [t1, t2])
        t1.parent = t2.parent = tree
        # print(f"{t1} + {t2}")

        while tree.reduce():
            # print("Reduce", tree)
            pass

    return tree.magnitude


def f2(input):
    input = [parse_tree(eval(line)) for line in input]
    max_magnitude = -1
    for i in range(len(input)):
        for j in range(len(input)):
            if i == j:
                continue
            t1 = deepcopy(input[i])
            t2 = deepcopy(input[j])
            tree = Node(None, [t1, t2])
            t1.parent = t2.parent = tree
            max_magnitude = max(max_magnitude, tree.reduced().magnitude)
    return max_magnitude

