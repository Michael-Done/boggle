# game_coordinator.py
import random
from datetime import datetime
from .game import *

class GameCoordinator:
    def __init__(self):
        self.game_list = dict()

    def new_game(self):
        new_game_id = GameCoordinator.__generate_game_id()

        while(new_game_id in self.game_list):
            new_game_id = GameCoordinator.__generate_game_id()

        self.game_list[new_game_id] = Game(new_game_id)
        print(self.game_list)
        return new_game_id

    def flush_inactive_games(self):
        for g in dict(self.game_list).keys():
            age_seconds = (datetime.now() - self.game_list[g].time_touched).total_seconds()
            if age_seconds > GAME_TIMEOUT:
                self.game_list.pop(g)

    @staticmethod
    def __generate_game_id():
        game_id = ""
        for _ in range(6):
            r = 0
            if(random.randint(0,1)):
                r = random.randint(ord('A'), ord('Z'))
            else:
                r = random.randint(ord('1'), ord('9'))
            game_id += chr(r)

        return game_id
