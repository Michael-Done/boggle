# player.py
from datetime import datetime

PLAYER_TIMEOUT = 4

class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.score = 0