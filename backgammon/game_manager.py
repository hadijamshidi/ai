import numpy as np
from itertools import product


class Backgammon(object):
    """docstring for Game"""

    def __init__(self, name="Backgammon", start=1):
        self.name = name
        self.state = [0 for _ in range(28)]
        self.side = 0
        self.pair_counter = 0
        self.result = dict(finished=False, msg=None)
        self.start = start
        self.state[start + 0] = 2
        self.state[start + 11] = 5
        self.state[start + 16] = 3
        self.state[start + 18] = 5

        self.state[start + 23] = -2
        self.state[start + 12] = -5
        self.state[start + 7] = -3
        self.state[start + 5] = -5

    def turn_manager(self, dice_pair=None):
        self.test()
        if self.side == 0:
            self.side = np.random.choice([-1, 1])
            print("player:", self.side, "starts the game.")
            return
        if dice_pair[0] == dice_pair[1]:
            if self.pair_counter == 0:
                print("player: ", self.side, "had pair, it is his turn agian.")
                self.pair_counter += 1
                return
            else:
                print("player: ", self.side, "turn for pair finished.")
                self.pair_counter = 0
        self.side *= -1
        print("It is player: ", self.side, "turn.")
        return

    def all_dice(self):
        dice = [i for i in range(1, 7)]
        return list(product(dice, dice))

    def roll_dice(self):
        dice = list(np.random.choice([i for i in range(1, 7)], 2))
        if dice[0] == dice[1]:
            return [dice, dice]
        return [dice]

    def possible_moves(self, side, dice_result, current_state):
        final_result = []
        for dice in dice_result:
            result = []
            for i, state in enumerate(current_state[:-2]):
                if not side * state > 0:
                    continue
                # print("possible for dice:", dice, "move at: ", i)
                checking_possition = i + side * dice
                if not 0 < checking_possition < 25:
                    continue
                if side * current_state[checking_possition] < -1:
                    continue
                # print("we can move to", checking_possition)
                result.append([i, checking_possition])
            final_result.append(result if len(result) > 0 else [[0]])
        return list(product(final_result[0], final_result[1]))

    def possible_final_moves(self, side, dice_result, current_state):
        final_result = []
        for dice in dice_result:
            result = []
            for i, state in enumerate(current_state[:-2]):
                if not side * state > 0:
                    continue
                checking_possition = i + side * dice
                if side == 1:
                    if i > 24:
                        continue
                    if checking_possition > 24:
                        checking_possition = 26
                else:
                    if checking_possition < 1:
                        checking_possition = 27
                if side * current_state[checking_possition] < -1:
                    continue
                result.append([i, checking_possition])
            final_result.append(result if len(result) > 0 else [[0]])
        return list(product(final_result[0], final_result[1]))

    def move(self, side, movements, current_state=''):
        for movement in movements:
            if len(movement) == 1:
                continue
            position = movement[1]
            if side * self.state[position] < 0:
                self.hit(-side, position)
            self.state[movement[0]] -= side
            self.state[position] += side

    def hit(self, side, position):
        idx = 0 if side == 1 else 25
        print("hiting:", side, "at:", position, "moving to:", idx)
        self.state[idx] += side
        self.state[position] -= side

    def check_status(self, side):
        idx = self.get_outbox_index(side)
        if self.state[idx] != 0:
            return 'out'
        index_range = range(self.start + 18) if side == 1 else range(self.start + 6, 26)
        for i in index_range:
            if side * self.state[i] > 0:
                return 'normal'
        return 'final'

    def get_outbox_index(self, side):
        return 0 if side == 1 else 25

    def check_moves(self, movements, side, status):
        # print("checking movements: 00000000000000")
        # print("checking movements:\n", len(movements), movements)
        moves = []
        for movement in movements:
            # print(movement, movement[0], movement[1], movement[0][0], movement[1][0])
            if movement[0][0] == movement[1][0]:
                if side * self.state[movement[0][0]] > 1:
                    moves.append(movement)
                else:
                    # print("rejecting:", movement)
                    moves.append([movement[0], [0]])
                    moves.append([[0], movement[1]])
            else:
                moves.append(movement)
        movements = moves
        # print("accepted:", len(movements), movements)
        if status in ['final', 'normal']:
            return movements
        idx = self.get_outbox_index(side)
        entrace_moves = list(filter(lambda x: x[0][0] == idx or x[1][0] == idx, movements))
        if side * self.state[idx] == 1:
            return entrace_moves
        return list(filter(lambda x: x[0][0] == idx and x[1][0] == idx, entrace_moves))

    def get_movements(self, side, dice_pair):
        status = self.check_status(side)
        movements = self.possible_moves(side=side, dice_result=dice_pair, current_state=self.state)
        if status == 'final':
            movements = self.possible_final_moves(side=side, dice_result=dice_pair, current_state=self.state)
        # return self.check_moves(movements, side, status)
        return self.check_moves(movements, side, status)

    def choice_move(self, movements, side):
        print("movements:", len(movements), movements)
        return movements[0]

    def play(self, side):
        dice_pairs = self.roll_dice()
        print("dices:", dice_pairs)
        for dice_pair in dice_pairs:
            print("dice:", dice_pair)
            movements = self.get_movements(side=side, dice_pair=dice_pair)
            if len(movements) == 0:
                # print(self.state)
                print("there is no move!")
                self.turn_manager(dice_pair=dice_pair)
                return 0
            move = self.choice_move(movements, side)
            # print("dice:", dice_pair, "\nmovements:", movements, "\nour move:", move)
            print("our move:", move)
            self.move(side, move)
            print(self.state)
            self.turn_manager(dice_pair=dice_pair)

    def test(self):
        if self.state[26] == 15:
            self.result = dict(finished=True, msg="player 1 won!")
            # raise Exception("player 1 won!")
        if self.state[27] == -15:
            self.result = dict(finished=True, msg="player -1 won!")
            # raise Exception("player -1 won!")
        if self.state[0] < 0:
            self.result = dict(finished=True, msg="-1 side at: 0")
            # raise Exception("-1 side at: 0")
        if self.state[25] > 0:
            self.result = dict(finished=True, msg="1 side at: 25")
            # raise Exception("1 side at: 25")
        for side in [-1, 1]:
            guys = filter(lambda x: x * side > 0, self.state)
            if side * sum(guys) != 15:
                self.result = dict(finished=True, msg="how many guys for: {} ??")
                # raise Exception("how many guys for: {} ??".format(side))


def run():
    game = Backgammon()
    print(game.state)
    game.turn_manager()
    for i in range(100):
        game.play(game.side)
        if game.result['finished']:
            print(game.result['msg'])
            break


run()
