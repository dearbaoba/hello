
def rc2n(r, c):
    return r * 3 + c


class Point(object):

    def __init__(self):
        self.moves = [0 for i in range(9)]
        self.winner = 0

    def __is_r(self, r, c, player):
        for i in range(3):
            if self.moves[rc2n(r, (c + i) % 3)] != player:
                return False
        return True

    def __is_c(self, r, c, player):
        for i in range(3):
            if self.moves[rc2n((r + i) % 3, c)] != player:
                return False
        return True

    def __is_rc(self, r, c, player):
        for i in range(3):
            if self.moves[rc2n((r + i) % 3, (c + i) % 3)] != player:
                return False
        return True

    def __is_winner(self, r, c, player):
        if self.__is_r(r, c, player) or self.__is_c(r, c, player) or self.__is_rc(r, c, player):
            self.winner = player
        return self.winner

    def move(self, r, c, player):
        self.moves[rc2n(r, c)] = player
        return self.__is_winner(r, c, player)

    def get_moves(self, R, C):
        moves = []
        if self.winner == 0:
            for n, item in enumerate(self.moves):
                if item == 0:
                    moves.append((R, C, int(n / 3), n % 3))
        return moves


class Rule(object):

    def __init__(self):
        self.big_point = Point()
        self.small_point = [Point() for i in range(9)]

    def __get_moves(self, r, c):
        moves = self.small_point[rc2n(r, c)].get_moves(r, c)
        if len(moves) == 0:
            for (_, _, R, C) in self.big_point.get_moves(r, c):
                moves2 = self.small_point[rc2n(R, C)].get_moves(R, C)
                for item in moves2:
                    moves.append(item)
        return moves

    def move(self, (R, C, r, c), player):
        is_win = self.small_point[rc2n(R, C)].move(r, c, player)
        if is_win:
            return self.big_point.move(R, C, player), self.__get_moves(r, c)
        return False, self.__get_moves(r, c)


def play_one():
    import random

    winner = False
    moves = []
    rule = Rule()
    winner, moves = rule.move((0, 0, 0, 0), 1)
    steps = 1
    while not winner:
        if len(moves) == 0:
            # print "draw"
            return 0
        n = int(random.uniform(0, len(moves)))
        # print moves[n]
        winner, moves = rule.move(moves[n], steps % 2 + 1)
        steps += 1
        # print rule.big_point.moves
    # print "winner is " + str((steps - 1) % 2 + 1)
    return (steps - 1) % 2 + 1

import time

begin = time.time()
result = [0 for i in range(3)]
while True:
    result[play_one()] += 1
    now = time.time() - begin
    if now > 1:
        break
print result
