# player.py
from datetime import datetime
from enum import Enum
import requests

PLAYER_TIMEOUT = 4

class WordState(Enum):
    VALID = 0
    TOO_SHORT = 1
    NOT_A_WORD = 2


class Player:
    def __init__(self, player_name):
        self.name = player_name
        self.score = 0
        self.words = {}

    def add_word(self, word, min_length):
        word = word.strip().lower()

        if len(word) < min_length:
            self.words[word] = WordState.TOO_SHORT
            return

        resp = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + word)
        print(resp.json())
