import requests
import json
import time
import random
import copy


move_map = []
move_tree = {}


def send(data):
    github_url = "http://10.9.88.20:8080/alphattt.yaws"
    cookies = {"SID": "nonode@nohost-288866164725755771148025299283002019618"}
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
    begin = time.time()
    num = 0
    rule = Rule()
    now = 0
    for move, player in move_map:
        result, legal_moves = rule.move(move, player)
    while True:
        num += 1
        winner, trace = random_search(rule, legal_moves)
        if winner == "I":
            inc_search_tree(trace, 1)
        else:
            inc_search_tree(trace, 0)
        now = time.time() - begin
        if now > 1:
            break
    node = move_tree
    if len(rule.move_trace) > 0:
        node = search_tree(rule.move_trace)
    final_move, cal, win, total = get_max_move(node, legal_moves)
    return [final_move[0], final_move[1], final_move[2], final_move[3]], cal, win, total, num, now, legal_moves


def get_max_move(node, legal_moves):
    final = {"per": 0, "win": 0, "total": 0, "move": None}
    for item in legal_moves:
        cal = node.get((item, "I"), None)
        if cal is not None:
            per = cal["win"] * 100 / cal["total"]
            if per > final["per"]:
                final["win"] = cal["win"]
                final["total"] = cal["total"]
                final["per"] = per
                final["move"] = item
    return final["move"], final["per"], final["win"], final["total"]


def search_tree(trace, index=0, tree=move_tree):
    if index < (len(trace) - 1) and tree is not None:
        return search_tree(trace, index + 1, tree[trace[index]]["tree"])
    return tree[trace[index]]["tree"]


def inc_search_tree(trace, is_win, index=0, tree=move_tree):
    if index < len(trace) - 1 and tree is not None:
        node = tree.get(trace[index], None)
        if node is None:
            tree[trace[index]] = {"win": is_win, "total": 1, "tree": {}}
        else:
            node["total"] += 1
            node["win"] += is_win
        inc_search_tree(trace, is_win, index + 1, tree[trace[index]]["tree"])


def random_search(rule, legal_moves):
    _rule = copy.deepcopy(rule)
    moves = legal_moves
    while True:
        is_win, moves = _rule.move(random_move(moves), "I")
        if is_win:
            return "I", _rule.move_trace
        elif len(moves) == 0:
            return "None", _rule.move_trace
        is_win, moves = _rule.move(random_move(moves), "AI")
        if is_win:
            return "AI", _rule.move_trace
        elif len(moves) == 0:
            return "None", _rule.move_trace


def random_move(legal_moves):
    n = int(random.uniform(0, len(legal_moves)))
    if n > len(legal_moves):
        n = len(legal_moves)
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
        for i in range(3):
            if self.moves[rc2n((r + i) % 3, (c + i) % 3)] != player:
                return False
        return True

    def __is_cr(self, r, c, player):
        for i in range(3):
            if self.moves[rc2n((r + i) % 3, (c - i) % 3)] != player:
                return False
        return True

    def __is_winner(self, r, c, player):
        if self.__is_r(r, c, player) or self.__is_c(r, c, player) \
                or self.__is_rc(r, c, player) or self.__is_cr(r, c, player):
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
                print "within:", legal_moves
                move_map.append(((move["R"], move["C"], move["r"], move["c"]), "AI"))
                # time.sleep(2)
            if len(legal_moves) > 0:
                i_move, per, win, total, num, now, legal_moves = get_move(legal_moves)
                print "I move:"
                print i_move, per, (win, total), num, now
                print "within:", legal_moves
                move_map.append(((i_move[0], i_move[1], i_move[2], i_move[3]), "I"))
                do_move(i_move)
            if steps > 5:
                break
        print "over."
    rule = Rule()
    result = False
    player = "None"
    final_move = None
    for final_move, player in move_map:
        result, _ = rule.move(final_move, player)
    print result, player, final_move
    # f = file("move_tree.pkl", "w")
    # pickle.dump(move_tree, f)
    # f.close()

if __name__ == '__main__':
    # try:
    #     f = file("move_tree.pkl", "r")
    #     move_tree = pickle.load(f)
    #     f.close()
    # except Exception, e:
    #     print e
    # while True:
    main()
