from backgammon.game_manager import Backgammon


class Simulator:
    def __init__(self, game):
        self.game = game()
        pass

    def run(self, moves_num=100):
        print(self.game.state)
        self.game.turn_manager()
        for i in range(moves_num):
            self.game.play(self.game.side)
            if self.game.result['finished']:
                print(self.game.result['msg'])
                break
        print("FINISHED")


def run_simulation():
    simulator = Simulator(game=Backgammon)
    simulator.run()
