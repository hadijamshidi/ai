from backgammon.game_manager import Backgammon
from itertools import product
import numpy as np


class Agent:
    target_side = 1
    default_future_factor = 10

    def __init__(self, game=Backgammon(), side=target_side, future_factor=default_future_factor):
        self.game = game
        self.game_snap = self.reset_game_snap(self.game)
        self.side = side
        self.current_reward = 0
        self.future_factor = future_factor

    def reset_game_snap(self, game):
        game_snap = Backgammon()
        for key, value in game.__dict__.items():
            game_snap.__setattr__(key, value)
        return game_snap

    def choice_move(self, movements, side):
        if not side == Agent.target_side:
            return self.default_move(movements)
        print("movements:", len(movements), movements)
        rewards = self.calc_all_movements_reward(movements)
        return self.get_highest_rewarded_movement(rewards)

    def get_highest_rewarded_movement(self, rewards):
        rewards_list = [r[0] for r in rewards]
        highest_reward = int(max(rewards_list))
        highest_rewarded_actions = list(filter(lambda x: x[0] == highest_reward, rewards))
        return highest_rewarded_actions[0][1]

    def calc_all_movements_reward(self, movements):
        ratings = []
        for movement in movements:
            ratings.append([self.calc_movement_reward(movement), movement])
        return ratings

    def calc_movement_reward(self, movement):
        return np.random.randint(10)

    def default_move(self, movements):
        return movements[0]
