# -*- coding: UTF-8 -*-
import requests
import json
import time
import random
import copy
import math

from pyboard import Board


cookie = {}
DEBUG = True
cal_time = 1


def send(data):
    global cookie
    # github_url = "http://10.8.39.80/alphattt.yaws"
    github_url = "http://10.9.88.20:8080/alphattt.yaws"
    # cookie = {"SID": "nonode@nohost-180628681594120732172449048974498269359"}
    data = json.dumps(data)
    r = requests.post(github_url, data, cookies=cookie)
    if r.cookies.get("SID", None) is not None:
        cookie["SID"] = r.cookies.get("SID", None)
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
                 "params": move2list(move)})["result"] == "ok"


def check(board=None):
    if DEBUG:
        move = random.choice(board.legal_moves)
        return move, [0]
    result = send({"id": "httpReq", "method": "get_state", "params": []})
    legal_moves = result.get("result", {}).get("legal_moves", [])
    move = result.get("result", {}).get("move", [])
    legal_moves = [dict2move(item) for item in legal_moves]
    if len(move) > 0:
        move = dict2move(move)
    return move, legal_moves


def random_pick(moves):
    n = random.randint(0, len(moves) - 1)
    return moves[n]


def move2list(move):  # (s, n) -> []
    N = math.log(move[0], 2)
    n = math.log(move[1], 2)
    return [int(N / 3), int(N % 3), int(n / 3), int(n % 3)]


def dict2move(data):
    (R, C, r, c) = (data["R"], data["C"], data["r"], data["c"])
    return (2 ** (R * 3 + C), 2 ** (r * 3 + c))


class TreeSearch(object):
    def __init__(self):
        super(TreeSearch, self).__init__()
        self.tree = {}

    def get_move(self, board):
        paras = {"begin": time.time(), "num": 0, "time": 0}
        if len(board.legal_moves) == 0:
            return None
        while True:
            paras["num"] += 1
            self.__inc_tree(self.__tree_path(board))
            paras["time"] = time.time() - paras["begin"]
            if paras["time"] > cal_time:
                break
        print "== calculate %d paths using %f seconds ==" % (paras["num"], paras["time"])
        return self.__search_tree(board)

    def __tree_path(self, board):
        _board = copy.deepcopy(board)
        _legal_moves = board.legal_moves
        curr_player = Board.PLAYER_ME
        move_trace = []
        while True:
            _board.move((random.choice(_legal_moves), curr_player))
            move_trace.append(_board.get_board())
            winner = _board.winner
            if winner is not None:
                return (move_trace, winner)
            _legal_moves = _board.legal_moves
            curr_player += 1
            curr_player = curr_player % 2

    def __inc_tree(self, (move_trace, winner)):
        inc = {"win": 0, "total": 1}
        if winner == Board.PLAYER_ME:
            inc["win"] = 1
        for item in move_trace:
            node = None
            try:
                node = self.tree[item]
            except Exception:
                self.tree[item] = {"win": 0, "total": 0}
                node = self.tree[item]
            node["win"] += inc["win"]
            node["total"] += inc["total"]

    def __search_tree(self, board):
        final = {"per": 0, "win": 0, "total": 0, "move": None}
        for move in board.legal_moves:
            _board = copy.deepcopy(board)
            _board.move((move, Board.PLAYER_ME))
            node = self.tree.get(_board.get_board(), None)
            wins = node["win"] * 100 / node["total"]
            if wins >= final["per"]:
                final["per"] = wins
                final["win"] = node["win"]
                final["total"] = node["total"]
                final["move"] = move
        print "== probability is %d. %d/%d ==" % (final["per"], final["win"], final["total"])
        return final["move"]


def main(tree):
    if start():
        print "start"
        time.sleep(3)
        board = Board()
        while True:
            move, legal_moves = check(board)
            if len(move) == 0 and len(legal_moves) == 0:
                time.sleep(1)
                continue
            if len(move) > 0:
                board.move((move, Board.PLAYER_AI))
                print "A move:"
                board.paint()
            if len(legal_moves) > 0:
                i_move = tree.get_move(board)
                if i_move is not None:
                    board.move((i_move, Board.PLAYER_ME))
                    do_move(i_move)
                    print "I move:"
                    board.paint()
            winner = board.winner
            if winner is not None:
                return winner

if __name__ == '__main__':
    import cProfile

    wins = {"win": 0, "total": 0, "draw": 0}
    players = ["I", "A"]
    num = 0
    while True:
        num += 1
        if num > 30:
            break
        tree = TreeSearch()
        if DEBUG:
            print cProfile.run("main(tree)")
            break
        winner = main(tree)
        if winner == Board.PLAYER_ME:
            wins["win"] += 1
        if winner == Board.PLAYER_NO:
            wins["draw"] += 1
        else:
            wins["total"] += 1
        print "winner is " + players[winner]
        print "total: %d/%d draw: %d nodes: %d" % \
            (wins["win"], wins["total"], wins["draw"], len(tree.tree))
