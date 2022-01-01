# player.py
from datetime import datetime
from enum import Enum
import requests

PLAYER_TIMEOUT = 4

class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.score = 0
        self.words = []

    def add_word(self, word):
        self.words.append(word)

