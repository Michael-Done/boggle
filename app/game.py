# game.py
from datetime import datetime
import random
from enum import Enum
from math import floor
import requests
from .player import Player
from .dice import dice16, dice25

GAME_TIMEOUT = 60*5 # Five minutes

class GameState(Enum):
    SETUP = 0
    ROUND_START = 1
    ROUND_ACTIVE = 2
    ROUND_END = 3

class WordState(Enum):
    VALID = 0
    TOO_SHORT = 1
    NOT_A_WORD = 2

class Game:
    def __init__(self, game_id):
        self.player_list = {}

        self.settings = {
            'board_size': 4,
            'word_length': 3,
            'round_timer': 60*3,
            'accepted_types': [
                'noun',
                'verb',
                'adjective',
                'adverb'
            ]
        }
        
        self.id = game_id
        self.state = GameState.ROUND_START

        self.time_created = datetime.now()
        self.touch()

        print("Game", self.id, "created at", self.time_created)
    
    def get_state(self):
        current_state = {
            'state': self.state.name,
            'players': list(self.player_list.keys()),
        }
        if hasattr(self, 'board'):
            current_state['board'] = self.board

        return current_state

    def touch(self):
        self.time_touched = datetime.now()

    def add_player(self, player_name):
        if player_name in self.player_list:
            return None
        else:
            self.player_list[player_name] = Player(player_name)
            return self.player_list[player_name]

    def add_word(self, player_name, word):
        word = word.strip().lower()

        if len(word) < self.settings['word_length']:
            return WordState.TOO_SHORT

        resp = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/' + word).json()
        print(resp)

        if 'title' in resp and resp['title'] == 'No Definitions Found':
            return WordState.NOT_A_WORD
        
        for w in resp:
            if w['word'] == word:
                meanings = w['meanings']
                for m in meanings:
                    if m['partOfSpeech'] in self.settings['accepted_types']:
                        self.player_list[player_name].add_word(word)
                        return WordState.VALID

        return WordState.NOT_A_WORD

    def new_round(self):
        self.touch()
        self.board = []
        dice = []
        if self.settings['board_size'] == 4:
            random.shuffle(dice16)
            dice = dice16
        elif self.settings['board_size'] == 5:
            random.shuffle(dice25)
            dice = dice25
        die = 0
        for row in range(self.settings['board_size']):
            self.board.append([])
            for col in range(self.settings['board_size']):
                self.board[row].append('?')
                self.board[row][col] = dice[die][random.randint(0,5)]
                die += 1
        self.state = GameState.ROUND_START

    def start_round(self):
        print(self.id + ': Round started')
        self.state = GameState.ROUND_ACTIVE
        self.time_started = datetime.now()

    def end_round(self):
        print(self.id + ': Round ended')
        self.state = GameState.ROUND_END

    def ping(self):
        delta = (datetime.now() - self.time_started).total_seconds()
        if delta >= self.settings['round_timer']:
            self.end_round()

    def get_time(self):
        time = self.settings['round_timer']

        if self.state == GameState.ROUND_ACTIVE:
            time -= (datetime.now() - self.time_started).total_seconds()
        elif self.state == GameState.ROUND_END:
            time = 0

        sec = floor(time % 60)
        return (str(floor(time/60)) + ':' + f'{sec:02}')

    @staticmethod
    def __score(self, letter_count):
        if letter_count == 3 or letter_count == 4:
            return 1
        elif letter_count == 5:
            return 2
        elif letter_count == 6:
            return 3
        elif letter_count == 7:
            return 5
        elif letter_count >= 8:
            return 11
        else:
            return 0