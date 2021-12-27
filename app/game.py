# game.py
from datetime import datetime
from .player import Player

class Game:
    def __init__(self, game_id):
        self.player_list = {}
        self.id = game_id
        self.time_created = datetime.now()
        self.touch()
        print("Game", self.id, "created at", self.time_created)

    def touch(self):
        self.time_touched = datetime.now()

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
