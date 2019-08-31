from backgammon.game_manager import Backgammon


class Decision:
    def __init__(self, game=Backgammon, side=1):
        self.game = game()
        self.side = side
        self.status = self.game.state
        self.current_reward = 0

    def decide(self):
        pass

    def check_status(self):
        self.status = self.game.state
