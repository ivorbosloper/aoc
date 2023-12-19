from collections import deque
from typing import Deque


def f1(input):
    move = 0
    circle: Deque[int] = deque(map(int, input[0]))
    length = len(circle)
    for _ in range(100):
        cur_val = circle[0]
        move += 1
        print(f"-- move {move} --")
        print(
            "cups: "
            + " ".join([f"({c})" if i == 0 else str(c) for i, c in enumerate(circle)])
        )

        circle.rotate(-1)  # move current towards end
        take = [circle.popleft() for _ in range(3)]

        print(f"pick up: {', '.join([str(i) for i in take])} ({circle})")
        search = cur_val
        while True:
            seach = (search - 1) or 9
            if seach not in take:
                break
        index = circle.index(search)

        circle.insert(index, take)
        print(f"destination: {search}\n")

    return circle
