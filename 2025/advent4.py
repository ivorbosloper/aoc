from util import BaseBoard, HZD_VARIANTS


class Board(BaseBoard):
    def solve(self, nr=4):
        total = 0
        for y, row in enumerate(self.board):
            for x, e in enumerate(row):
                if e != '@':
                    continue
                total += sum(self.get(x+dx, y+dy) == '@' for dx, dy in HZD_VARIANTS) < nr

        return total


    def solve2(self, nr=4):
        total = 0
        while True:
            results = []
            for y, row in enumerate(self.board):
                for x, e in enumerate(row):
                    if e != '@':
                        continue
                    if sum(self.get(x+dx, y+dy) == '@' for dx, dy in HZD_VARIANTS) < nr:
                        results.append((x, y))
            for x, y in results:
                self.board[y][x] = '.'
            if len(results) == 0:
                break
            total += len(results)

        return total

def f2(input):
    board = Board(input)
    return board.solve2()
