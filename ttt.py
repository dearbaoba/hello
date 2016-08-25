import requests
import json
import time
import random
import copy
import cPickle as pickle


move_map = []
move_tree = {}
cal_time = 1


def send(data):
    github_url = "http://10.9.88.20:8080/alphattt.yaws"
    cookies = {"SID": "nonode@nohost-32302372811942131573818954210653580022"}
    data = json.dumps(data)
    r = requests.post(github_url, data, cookies=cookies)
    # print r.json()
    return r.json()


def start():
    return send({"id": "httpReq", "method": "start_game", "params": []})["result"] == "ok"


def do_move(move):
    return send({"id": "httpReq", "method": "set_move", "params": move})["result"] == "ok"


def check():
    result = send({"id": "httpReq", "method": "get_state", "params": []})
    return result.get("result", []).get("legal_moves", []), result.get("result", []).get("move", [])


def get_move(legal_moves):
    paras = {"begin": time.time(), "num": 0, "time": 0}
    rule = Rule()
    for move, player in move_map:
        result, legal_moves = rule.move(move, player)
        if result:
            return None, None
    while True:
        paras["num"] += 1
        winner, trace = random_search(rule, legal_moves)
        if winner == "I":
            inc_search_tree(trace, 1)
        elif winner == "A":
            inc_search_tree(trace, 0)
        paras["time"] = time.time() - paras["begin"]
        if paras["time"] > cal_time:
            break
    final_move = get_max_move(search_tree(rule.move_trace), legal_moves)
    print "== calculate %d paths using %f seconds ==" % (paras["num"], paras["time"])
    return list(final_move), legal_moves


def get_max_move(node, legal_moves):
    final = {"per": 0, "win": 0, "total": 0, "move": None, "legal_moves": legal_moves, "cal": []}
    for item in legal_moves:
        cal = node.get(item, None)
        if cal is not None:
            final["cal"].append(cal)
            per = cal["win"] * 100 / cal["total"]
            if per > final["per"]:
                final["win"] = cal["win"]
                final["total"] = cal["total"]
                final["per"] = per
                final["move"] = item
    print "== probability is %d. %d/%d ==" % (final["per"], final["win"], final["total"])
    for i in range(len(final["cal"])):
        print "%s :: %s %d" % \
            (str(final["legal_moves"][i]),
                str((final["cal"][i]["win"], final["cal"][i]["total"])),
                final["cal"][i]["win"] * 100 / final["cal"][i]["total"])
    return final["move"]


def search_tree(trace, index=0, tree=move_tree):
    if len(trace) == 0:
        return tree
    if index < (len(trace) - 1) and tree is not None:
        return search_tree(trace, index + 1, tree[trace[index][0]]["tree"])
    return tree[trace[index][0]]["tree"]


def inc_search_tree(trace, is_win, index=0, tree=move_tree):
    if index < len(trace) and tree is not None:
        node = tree.get(trace[index][0], None)
        if node is None:
            tree[trace[index][0]] = {"win": is_win, "total": 1, "tree": {}}
        else:
            node["total"] += 1
            node["win"] += is_win
        inc_search_tree(trace, is_win, index + 1, tree[trace[index][0]]["tree"])


def random_search(rule, legal_moves):
    _rule = copy.deepcopy(rule)
    moves = legal_moves
    players = ["I", "A"]
    curr = 0
    while True:
        is_win, moves = _rule.move(random_move(moves), players[curr])
        if is_win:
            return players[curr], _rule.move_trace
        elif len(moves) == 0:
            return "None", _rule.move_trace
        curr = (curr + 1) % 2


def random_move(legal_moves):
    if len(legal_moves) == 0:
        print len(legal_moves)
        raise "error len"
    n = random.randint(0, len(legal_moves) - 1)
    return legal_moves[n]


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
        if r != c:
            return False
        for i in range(3):
            if self.moves[rc2n((r + i) % 3, (c + i) % 3)] != player:
                return False
        return True

    def __is_cr(self, r, c, player):
        if (r + c) != 2:
            return False
        for i in range(3):
            if self.moves[rc2n((r + i) % 3, (c - i) % 3)] != player:
                return False
        return True

    def __is_winner(self, r, c, player):
        if self.__is_r(r, c, player) \
                or self.__is_c(r, c, player) \
                or self.__is_rc(r, c, player) \
                or self.__is_cr(r, c, player):
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
        self.move_trace = []

    def __get_moves(self, r, c):
        moves = self.small_point[rc2n(r, c)].get_moves(r, c)
        if len(moves) == 0:
            for (_, _, R, C) in self.big_point.get_moves(r, c):
                moves2 = self.small_point[rc2n(R, C)].get_moves(R, C)
                for item in moves2:
                    moves.append(item)
        return moves

    def move(self, (R, C, r, c), player):
        self.move_trace.append(((R, C, r, c), player))
        is_win = self.small_point[rc2n(R, C)].move(r, c, player)
        if is_win:
            return self.big_point.move(R, C, player), self.__get_moves(r, c)
        return False, self.__get_moves(r, c)


def draw_final():
    rule = Rule()
    moves = ["0" for i in range(9 * 9)]
    final = "draw", "None"
    line = [["N" for i in range(9)], ["N" for i in range(9)], ["N" for i in range(9)],
            ["N" for i in range(9)], ["N" for i in range(9)], ["N" for i in range(9)],
            ["N" for i in range(9)], ["N" for i in range(9)], ["N" for i in range(9)]]
    for move, player in move_map:
        moves[move[0] * 27 + move[1] * 9 + move[2] * 3 + move[3]] = player
        if rule.move(move, player)[0]:
            final = "%s win!" % player, player
    for R in range(3):
        for r in range(3):
            for C in range(3):
                for c in range(3):
                    line[R * 3 + r][C * 3 + c] = moves[R * 27 + C * 9 + r * 3 + c]
    for i in range(9):
        print "%s %s %s  %s %s %s  %s %s %s" % \
            (line[i][0], line[i][1], line[i][2],
                line[i][3], line[i][4], line[i][5],
                line[i][6], line[i][7], line[i][8])
        if (i + 1) % 3 == 0:
            print "---"
    return final


def main():
    if start():
        print "start"
        time.sleep(3)
        steps = 0
        while True:
            legal_moves, move = check()
            legal_moves = [(m["R"], m["C"], m["r"], m["c"]) for m in legal_moves]
            steps += 1
            if len(move) == 0 and len(legal_moves) == 0:
                time.sleep(1)
            if len(move) > 0:
                steps = 0
                print "AI move:"
                print [move["R"], move["C"], move["r"], move["c"]]
                print "Give:", legal_moves
                move_map.append(((move["R"], move["C"], move["r"], move["c"]), "A"))
                draw_final()
            if len(legal_moves) > 0:
                i_move, legal_moves = get_move(legal_moves)
                if i_move is None:
                    break
                print "I move:"
                print i_move
                print "With:", legal_moves
                move_map.append((tuple(i_move), "I"))
                do_move(i_move)
                draw_final()
            if steps > 5:
                break
        print "over."
    return draw_final()


if __name__ == '__main__':
    try:
        f = file("move_tree.pkl", "r")
        move_tree = pickle.load(f)
        f.close()
    except Exception, e:
        print e
    wins = {"win": 0, "total": 0}
    while True:
        move_map = []
        result, player = main()
        wins["total"] += 1
        if player == "I":
            wins["win"] += 1
        print result
        print "total: %d/%d" % (wins["win"], wins["total"])
        f = file("move_tree.pkl", "w")
        pickle.dump(move_tree, f)
        f.close()
