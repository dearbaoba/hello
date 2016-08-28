import requests
import json
import time
import random
import copy


PLAYER_ME = "I"
PLAYER_AI = "A"
PLAYER_NO = "N"

move_tree = {}
cal_time = 1
cookie = {}
DEBUG = True


def send(data):
    global cookie
    github_url = "http://10.9.88.20:8080/alphattt.yaws"
    # cookie = {"SID": "nonode@nohost-180628681594120732172449048974498269359"}
    data = json.dumps(data)
    r = requests.post(github_url, data, cookies=cookie)
    if r.cookie.get("SID", None) is not None:
        cookie["SID"] = r.cookie.get("SID", None)
        print cookie
    # print r.json()
    return r.json()


def start():
    if DEBUG:
        return True
    return send({"id": "httpReq", "method": "start_game", "params": []})["result"] == "ok"


def do_move(move):
    if DEBUG:
        return True
    return send({"id": "httpReq", "method": "set_move",
                 "params": list(n2RCrc(move[0]))})["result"] == "ok"


def check(rule=None):
    if DEBUG:
        move = pick_move(rule.get_legal_moves(), PLAYER_AI)
        return move, [0]
    result = send({"id": "httpReq", "method": "get_state", "params": []})
    legal_moves = result.get("result", {}).get("legal_moves", [])
    move = result.get("result", {}).get("move", [])
    legal_moves = [RCrc2n(item["R"], item["C"], item["r"], item["c"]) for item in legal_moves]
    move = (RCrc2n(move["R"], move["C"], move["r"], move["c"]), PLAYER_AI)
    return move, legal_moves


def get_move(rule):
    paras = {"begin": time.time(), "num": 0, "time": 0}
    legal_moves = rule.get_legal_moves()
    if legal_moves == []:
        return None
    while True:
        paras["num"] += 1
        inc_tree(tree_path(rule, legal_moves))
        paras["time"] = time.time() - paras["begin"]
        if paras["time"] > cal_time:
            break
    print "== calculate %d paths using %f seconds ==" % (paras["num"], paras["time"])
    return search_tree(rule.moves, legal_moves)


def inc_tree((trace, winner)):
    inc = {"win": 0, "total": 1}
    if winner == PLAYER_ME:
        inc["win"] = 1
    moves = [0 for i in range(81)]
    for (n, player) in trace:
        moves[n] = 1
        node = move_tree.get((tuple(moves), n), None)
        if node is None:
            move_tree[(tuple(moves), n)] = {"win": 0, "total": 0}
            node = move_tree[(tuple(moves), n)]
        node["win"] += inc["win"]
        node["total"] += inc["total"]


def search_tree(moves, legal_moves):
    final = {"per": 0, "win": 0, "total": 0, "move": None}
    for n in legal_moves:
        _moves = copy.copy(moves)
        _moves[n] = 1
        node = move_tree.get((tuple(_moves), n), None)
        wins = node["win"] * 100 / node["total"]
        if wins >= final["per"]:
            final["per"] = wins
            final["win"] = node["win"]
            final["total"] = node["total"]
            final["move"] = (n, PLAYER_ME)
    print "== probability is %d. %d/%d ==" % (final["per"], final["win"], final["total"])
    return final["move"]


def tree_path(rule, legal_moves):
    _rule = copy.deepcopy(rule)
    _legal_moves = legal_moves
    players = [PLAYER_ME, PLAYER_AI]
    curr = 0
    while True:
        _rule.move(pick_move(_legal_moves, players[curr]))
        winner = _rule.winner()
        if winner is not None:
            return _rule.move_trace, winner
        _legal_moves = _rule.get_legal_moves()
        curr += 1
        curr = curr % 2


def pick_move(legal_moves, player):
    n = random.randint(0, len(legal_moves) - 1)
    return (legal_moves[n], player)


def RCrc2n(R, C, r, c):
    return R * 27 + C * 9 + r * 3 + c


def n2RCrc(n):
    R = int(n / 27)
    C = int(n % 27 / 9)
    t = n % 9
    r = int(t / 3)
    c = int(t % 3)
    return (R, C, r, c)


class Point(object):

    def __init__(self):
        self.moves = [None for i in range(9)]
        self.curr_move = None

    def winner(self):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for win in wins:
            if self.moves[win[0]] == self.moves[win[1]] \
                    and self.moves[win[1]] == self.moves[win[2]] \
                    and self.moves[win[0]] is not None \
                    and self.moves[win[0]] != PLAYER_NO:
                return self.moves[win[0]]
        for item in self.moves:
            if item is None:
                return None
        return PLAYER_NO

    def get_legal_moves(self):
        legal_moves = []
        if self.winner() is None:
            for i, item in enumerate(self.moves):
                if item is None:
                    legal_moves.append(i)
        return legal_moves

    def move(self, (n, player)):
        self.curr_move = (n, player)
        self.moves[n] = player


class Rule(object):

    def __init__(self):
        self.moves = [0 for i in range(81)]
        self.move_trace = []
        self.curr_move = None
        self.big_point = Point()
        self.small_point = [Point() for i in range(9)]

    def __update_points(self):
        (n, player) = self.curr_move
        point = self.small_point[int(n / 9)]
        point.move((n % 9, player))
        winner = point.winner()
        if winner is not None:
            if winner == PLAYER_NO:
                self.big_point.move((int(n / 9), PLAYER_NO))
            else:
                self.big_point.move((int(n / 9), player))

    def winner(self):
        return self.big_point.winner()

    def get_legal_moves(self):
        if self.curr_move is None:
            return [0]
        n = self.curr_move[0] % 9
        moves = [i + n * 9 for i in self.small_point[n].get_legal_moves()]
        if moves == []:
            for index, item in enumerate(self.small_point):
                moves.extend([i + index * 9 for i in item.get_legal_moves()])
        return moves

    def move(self, (n, player)):
        self.curr_move = (n, player)
        self.move_trace.append(self.curr_move)
        self.moves[n] = 1
        self.__update_points()

    def print_game(self):
        print self.curr_move[1] + " move:"
        print n2RCrc(self.curr_move[0])

        moves = ["0" for i in range(81)]
        line = [["0" for i in range(9)] for j in range(9)]
        for (n, player) in self.move_trace:
            moves[n] = player
        for R in range(3):
            for r in range(3):
                for C in range(3):
                    for c in range(3):
                        line[R * 3 + r][C * 3 + c] = moves[R * 27 + C * 9 + r * 3 + c]
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


def main():
    if start():
        print "start"
        time.sleep(3)
        rule = Rule()
        while True:
            move, legal_moves = check(rule)
            if len(move) == 0 and len(legal_moves) == 0:
                time.sleep(1)
                continue
            if len(move) > 0:
                rule.move(move)
                rule.print_game()
            if len(legal_moves) > 0:
                i_move = get_move(rule)
                if i_move is not None:
                    rule.move(i_move)
                    do_move(i_move)
                    rule.print_game()
            winner = rule.winner()
            if winner is not None:
                return winner


if __name__ == '__main__':
    wins = {"win": 0, "total": 0}
    while True:
        winner = main()
        if winner == PLAYER_ME:
            wins["win"] += 1
        if winner != PLAYER_NO:
            wins["total"] += 1
        print "winner is " + winner
        print "total: %d/%d nodes: %d" % (wins["win"], wins["total"], len(move_tree))
