from backgammon.game_manager import Backgammon
from itertools import product
import numpy as np


class Agent:
    def __init__(self, game=Backgammon(), side=1):
        self.game = game
        self.game_snap = Backgammon()
        for key, value in game.__dict__.items():
            self.game_snap.__setattr__(key, value)
        self.side = side
        self.current_reward = 0

    def decide(self):
        pass

    def choice_move(self, movements, side):
        print("movements:", len(movements), movements)
        return movements[0]
