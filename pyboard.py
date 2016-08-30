# -*- coding: UTF-8 -*-


class Board(object):

    PLAYER_ME = 0
    PLAYER_AI = 1
    PLAYER_NO = 2
    BOARDS = (1, 2, 4, 8, 16, 32, 64, 128, 256)
    WINS = (7, 56, 448, 73, 146, 292, 273, 84)
    MAX_BOARD = 511

    def __init__(self, copy_board=None):
        super(Board, self).__init__()
        self.board = {
            1: [0, 0, 0, [i for i in Board.BOARDS]],
            2: [0, 0, 0, [i for i in Board.BOARDS]],
            4: [0, 0, 0, [i for i in Board.BOARDS]],
            8: [0, 0, 0, [i for i in Board.BOARDS]],
            16: [0, 0, 0, [i for i in Board.BOARDS]],
            32: [0, 0, 0, [i for i in Board.BOARDS]],
            64: [0, 0, 0, [i for i in Board.BOARDS]],
            128: [0, 0, 0, [i for i in Board.BOARDS]],
            256: [0, 0, 0, [i for i in Board.BOARDS]]
        }
        self.bboard = [0, 0, 0]
        self.curr_player = Board.PLAYER_NO
        self.winner = None
        self.legal_moves = [(1, 1)]
        self.move_trace = []

    def __is_win(self, n):
        for i in Board.WINS:
            if (n & i) == i:
                return True
        return False

    def __get_legal_moves(self, n):
        self.legal_moves = []
        if self.winner is None:
            if self.board[n][3] != []:
                self.legal_moves = [(n, i) for i in self.board[n][3]]
            else:
                for s, item in self.board.iteritems():
                    if item[3] != []:
                        self.legal_moves.extend([(s, i) for i in item[3]])
        return self.legal_moves

    def move(self, ((s, n), player)):
        # move
        self.board[s][player] += n
        self.board[s][2] += n
        self.board[s][3].remove(n)
        self.curr_player = player
        self.move_trace.append(((s, n), player))
        # calculate
        if self.__is_win(self.board[s][player]):
            self.board[s][3] = []
            self.bboard[player] += s
            self.bboard[2] += s
            if self.__is_win(self.bboard[player]):
                self.winner = player
        elif self.board[s][2] == Board.MAX_BOARD:
            self.bboard[2] += s
        if self.bboard[2] == Board.MAX_BOARD \
                and self.winner is None:
            self.winner = Board.PLAYER_NO
        return self.winner, self.__get_legal_moves(n)

    def get_board(self):
        return tuple(self.move_trace)

    def paint(self):
        import math

        line = [["0" for i in xrange(9)] for i in xrange(9)]
        for s, board in self.board.iteritems():
            N = int(math.log(s, 2))
            for n in xrange(9):
                if ((board[0] >> n) & 1) == 1:
                    line[int(N / 3) * 3 + int(n / 3)][(N % 3) * 3 + n % 3] = "I"
                if ((board[1] >> n) & 1) == 1:
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
    board = Board()
    print board.board
    print board.move(((1, 1), Board.PLAYER_ME))
    print board.move(((1, 2), Board.PLAYER_ME))
    print board.move(((1, 4), Board.PLAYER_ME))
    print board.move(((2, 1), Board.PLAYER_AI))
    print board.move(((16, 2), Board.PLAYER_ME))
    print board.move(((16, 16), Board.PLAYER_ME))
    print board.move(((16, 128), Board.PLAYER_ME))
    print board.move(((256, 4), Board.PLAYER_ME))
    print board.move(((256, 16), Board.PLAYER_ME))
    print board.move(((256, 64), Board.PLAYER_ME))
    print board.get_board()
    board.paint()
