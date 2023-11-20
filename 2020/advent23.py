def f1(input):
    length = len(input[0])
    current = 0
    move = 0
    board = input[0]
    for _ in range(100):
        cur_val = board[current]
        move += 1
        print(f"-- move {move} --")
        print(
            "cups: "
            + " ".join([f"({c})" if i == current else c for i, c in enumerate(board)])
        )

        l, r = (current + 1) % length, (current + 4) % length
        if r < l:
            take = board[l:] + board[:r]
            board = board[r:l]
        else:
            take = board[l:r]
            board = board[:l] + board[r:]
        if r < current:
            current -= r

        print(f"pick up: {', '.join([str(i) for i in take])} ({board})")
        assert len(take) == 3
        search = "9" if cur_val == "1" else chr(ord(cur_val) - 1)
        while search not in board:
            search = "9" if search == "1" else chr(ord(search) - 1)
        index = board.index(search) + 1
        board = board[:index] + take + board[index:]
        if index <= current:
            current = (current + 3) % length
        assert board[current] == cur_val
        print(f"destination: {search}\n")
        current = (current + 1) % length

    index = board.index("1")
    return board[index + 1 :] + board[:index]
