from backgammon.agent import Agent
from backgammon.game_manager import Backgammon
from itertools import product
import numpy as np


class Simulator:
    def __init__(self, game=Backgammon):
        self.game = game()

    @staticmethod
    def all_dice():
        dice = [i for i in range(1, 7)]
        return list(product(dice, dice))

    @staticmethod
    def roll_dice():
        dice = list(np.random.choice([i for i in range(1, 7)], 2))
        if dice[0] == dice[1]:
            return [dice, dice]
        return [dice]

    def play(self, side):
        dice_pairs = Simulator.roll_dice()
        print("dices:", dice_pairs)
        for dice_pair in dice_pairs:
            print("dice:", dice_pair)
            movements = self.game.get_movements(side=side, dice_pair=dice_pair)
            if len(movements) == 0:
                print("there is no move!")
                self.game.turn_manager(dice_pair=dice_pair)
                return 0
            agent = Agent(game=self.game, side=side)
            move = agent.choice_move(movements, side)
            print("our move:", move)
            self.game.move(side, move)
            print(self.game.state)
            self.game.turn_manager(dice_pair=dice_pair)

    def run(self, moves_num=100):
        print(self.game.state)
        self.game.turn_manager()
        for i in range(moves_num):
            self.play(self.game.side)
            if self.game.result['finished']:
                print(self.game.result['msg'])
                break
        print("FINISHED")


def run_simulation():
    simulator = Simulator(game=Backgammon)
    simulator.run()
