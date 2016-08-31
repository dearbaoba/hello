# -*- coding: UTF-8 -*-


class Board(object):

    PLAYER_ME = 0
    PLAYER_AI = 1
    PLAYER_NO = 2
    BOARDS = (1, 2, 4, 8, 16, 32, 64, 128, 256)
    WINS = (7, 56, 448, 73, 146, 292, 273, 84)
    MAX_BOARD = 511
    POINTS = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2))

    def __init__(self, copy_board=None):
        super(Board, self).__init__()
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 2, 0, 0]
        self.overs = [0 for i in xrange(9)]

    def __is_win(self, n):
        for i in Board.WINS:
            if (n & i) == i:
                return True
        return False

    def move(self, ((R, C, r, c), player)):
        s, n = R * 3 + C, r * 3 + c
        winner = None
        S, N = Board.BOARDS[s], Board.BOARDS[n]
        # move
        self.board[s * 2 + player] += N
        self.board[20] = player
        self.board[21] = s
        self.board[22] = n
        # calculate
        if self.__is_win(self.board[s * 2 + player]):
            self.board[18 + player] += S
            self.overs[s] = 1
            if self.__is_win(self.board[18 + player]):
                winner = player
        elif (self.board[s * 2] + self.board[s * 2 + 1]) == Board.MAX_BOARD:
            self.overs[s] = 1
        if sum(self.overs) == 9 \
                and winner is None:
            winner = Board.PLAYER_NO
        return winner

    def get_legal_moves(self):
        def append_points(legal_moves, m, s):
            for i in xrange(9):
                if (m | (1 << i)) == m:
                    legal_moves.append((int(s / 3), int(s % 3), int(i / 3), int(i % 3)))
            return legal_moves

        legal_moves = []
        n = self.board[22]
        if self.overs[n] == 1:
            for index in xrange(9):
                m = Board.MAX_BOARD - self.board[index * 2] - self.board[index * 2 + 1]
                if self.overs[index] == 0:
                    legal_moves = append_points(legal_moves, m, index)
        else:
            m = Board.MAX_BOARD - self.board[n] - self.board[n + 1]
            legal_moves = append_points(legal_moves, m, n)
        return legal_moves

    def get_board(self):
        return tuple(self.board)

    def paint(self):
        line = [["0" for i in xrange(9)] for i in xrange(9)]
        for N in xrange(9):
            I = self.board[N * 2]
            A = self.board[N * 2 + 1]
            for n in xrange(9):
                if ((I >> n) & 1) == 1:
                    line[int(N / 3) * 3 + int(n / 3)][(N % 3) * 3 + n % 3] = "I"
                if ((A >> n) & 1) == 1:
                    line[int(N / 3) * 3 + int(n / 3)][(N % 3) * 3 + n % 3] = "A"
        for i in xrange(9):
            for j in xrange(9):
                if j == 8:
                    print line[i][j] + " "
                else:
                    print line[i][j] + " ",
                    if (j + 1) % 3 == 0:
                        print " ",
            if (i + 1) % 3 == 0:
                print "---"


if __name__ == '__main__':
    import random

    board = Board()
    print board.board
    print board.move(((0, 0, 0, 0), Board.PLAYER_ME))
    print board.get_legal_moves()
    print board.paint()
    print board.move(((0, 0, 0, 1), Board.PLAYER_ME))
    print board.move(((0, 0, 0, 2), Board.PLAYER_ME))
    print board.move(((0, 1, 0, 0), Board.PLAYER_AI))
    print board.get_legal_moves()
    print board.move(((1, 1, 0, 0), Board.PLAYER_ME))
    print board.move(((1, 1, 1, 0), Board.PLAYER_ME))
    print board.move(((1, 1, 2, 0), Board.PLAYER_ME))
    print board.move(((2, 2, 0, 2), Board.PLAYER_ME))
    print board.move(((2, 2, 1, 1), Board.PLAYER_ME))
    print board.move(((2, 2, 2, 0), Board.PLAYER_ME))
    print board.board
    print board.overs
    print board.paint()

    board2 = Board()
    player = 0
    while True:
        move = random.choice(board2.get_legal_moves())
        winner = board2.move((move, player))
        print player, move
        print board2.board
        print board2.overs
        print board2.get_legal_moves()
        board2.paint()
        player = (player + 1) % 2
        if winner is not None:
            print winner
            break
