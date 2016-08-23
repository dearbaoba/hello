
class Board(object):
    states = []  # 9
    winner = []  # 9

    def __init__(self):
        for i in range(9):
            state = State()
            self.states[i] = state

    def who_is_winner(self):
        pass

    def move(self, R, C, r, c, player):
        n = C * 3 + R
        moves, winner = self.states[n].next_state(r, c, player)
        self.winner[n] = winner
        return moves, self.who_is_winner()


class State(object):
    current = 0
    child_states = []  # 3^9

    def __init__(self):
        for n in range(3 ^ 9):
            state = ChildState(n)
            self.child_states[n] = state

    def next_state(self, r, c, player):
        self.current = self.child_states[self.current].next_state[player][r][c]
        child_state = self.child_states[self.current]
        return child_state.moves, child_state.winner


class ChildState(object):
    moves = []
    next_state = [[[[], [], []], [[], [], []], [[], [], []]],
                  [[[], [], []], [[], [], []], [[], [], []]]]
    winner = 0

    def __init__(self, n):
        pass
