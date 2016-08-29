# -*- coding: UTF-8 -*-

class Board(object):
    PLAYER_ME = 0
    PLAYER_AI = 1
    PLAYER_NO = 2
    BOARDS = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    WINS = [7, 56, 448, 73, 146, 292, 273, 84]
    MAX_BOARD = 511

    def __init__(self):
        super(Board, self).__init__()
        self.board = {
                                1: [0, 0, 0, Board.MAX_BOARD], 2: [0, 0, 0, Board.MAX_BOARD], 4: [0, 0, 0, Board.MAX_BOARD], 
                                8: [0, 0, 0, Board.MAX_BOARD],16: [0, 0, 0, Board.MAX_BOARD], 32: [0, 0, 0, Board.MAX_BOARD], 
                                64: [0, 0, 0, Board.MAX_BOARD], 128: [0, 0, 0, Board.MAX_BOARD], 256: [0, 0, 0, Board.MAX_BOARD], 
                                "bb": [0, 0, 0, Board.MAX_BOARD], "cp": [Board.PLAYER_NO]
                            }
        self.winner = None
        self.legal_moves = [(1, 1)]

    def __is_win(self, n):
        for i in Board.WINS:
            if (n & i) == i:
                return True
        return False

    def __get_legal_moves(self, n):
        def splite((n, move)):
            return filter(lambda (x, y): y > 0, [(n, move & (1 << i)) for i in range(9)])
        self.legal_moves = []
        if self.winner is None:
            if self.board[n][3] != 0:
                self.legal_moves = splite((n, self.board[n][3]))
            else:
                moves = filter(lambda (x, y): y != 0, [(i, self.board[i][3]) for i in Board.BOARDS])
                for item in moves:
                    self.legal_moves.extend(splite(item))
        return self.legal_moves

    def move(self, ((s, n), player)):
        # move
        self.board[s][player] += n
        self.board[s][2] += n
        self.board[s][3] -= n
        self.board["cp"][0] = player
        # calculate
        if self.__is_win(self.board[s][player]):
            self.board[s][3] = 0
            self.board["bb"][player] += s
            self.board["bb"][2] += s
            if self.__is_win(self.board["bb"][player]):
                self.winner = player
        elif self.board[s][2] == Board.MAX_BOARD:
            self.board["bb"][2] += s
        if self.board["bb"][2] == Board.MAX_BOARD:
            self.winner = Board.PLAYER_NO
        return self.winner, self.__get_legal_moves(n)

    def get_board(self):
        return tuple([tuple(item) for item in self.board.itervalues()])

    def paint(self):
        import math

        line = [["0" for i in range(9)] for i in range(9)]
        for s, board in self.board.iteritems():
            if s in Board.BOARDS:
                N = int(math.log(s, 2))
                for n in range(9):
                    if ((board[0] >> n) & 1) == 1:
                        line[int(N/3)*3+int(n/3)][(N%3)*3+n%3] = "I"
                    if ((board[1] >> n) & 1) == 1:
                        line[int(N/3)*3+int(n/3)][(N%3)*3+n%3] = "A"
        for i in range(9):
            for j in range(9):
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