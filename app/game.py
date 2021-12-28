# game.py
from datetime import datetime
from .player import PLAYER_TIMEOUT, Player

GAME_TIMEOUT = 60*5 # Five minutes

class Game:
    def __init__(self, game_id):
        self.player_list = {}
        self.id = game_id
        self.time_created = datetime.now()
        self.touch()
        print("Game", self.id, "created at", self.time_created)

    def touch(self):
        self.time_touched = datetime.now()
        for p in dict(self.player_list).keys():
            age_seconds = (self.time_touched - self.player_list[p].time_touched).total_seconds()
            print("player", p, age_seconds)
            if age_seconds > PLAYER_TIMEOUT:
                self.player_list.pop(p)

    def add_player(self, player_name):
        if player_name in self.player_list:
            return None
        else:
            self.player_list[player_name] = Player(player_name)
            return self.player_list[player_name]

    def get_player_by_ip(self, player_ip):
        for player in self.player_list:
            if self.player_list[player].ip == player_ip:
                return player
        return None
