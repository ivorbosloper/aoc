from util import HZD_VARIANTS, BaseBoard


class Board(BaseBoard):
    def simulate(self):
        queue = []
        for y, row in enumerate(self.board):
            for x in range(self.width):
                row[x] = e = row[x] + 1
                if e == 10:
                    queue.append((y, x))

        pointer = 0
        while pointer < len(queue):
            y, x = queue[pointer]
            pointer += 1
            for dy, dx in HZD_VARIANTS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width and self.board[ny][nx] < 10:
                    self.board[ny][nx] = e = self.board[ny][nx] + 1
                    if e == 10:
                        queue.append((ny, nx))

        for y, x in queue:
            self.board[y][x] = 0
        return len(queue)

    def all_same(self):
        base = self.board[0][0]
        return all(e == base for row in self.board for e in row)


def f1(input):
    board = Board(input)
    cnt = 0
    for i in range(100):
        cnt += board.simulate()
    return cnt

def f2(input):
    board = Board(input)
    cnt = 0
    while not board.all_same():
        board.simulate()
        cnt += 1
    return cnt
