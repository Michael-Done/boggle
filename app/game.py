# game.py
from datetime import datetime
import random
from enum import Enum
from .player import PLAYER_TIMEOUT, Player
from .dice import dice16

GAME_TIMEOUT = 60*5 # Five minutes

class GameState(Enum):
    SETUP = 0
    ROUND_START = 1
    ROUND_ACTIVE = 2
    ROUND_END = 3


class Game:
    def __init__(self, game_id):
        self.player_list = {}
        self.id = game_id
        self.state = GameState.SETUP
        self.time_created = datetime.now()
        self.round_timer = 60*3 # 3 minutes
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

    def get_player_by_ip(self, player_ip):
        for player in self.player_list:
            if self.player_list[player].ip == player_ip:
                return player
        return None

    def new_round(self):
        self.touch()
        self.board = [
            ['?', '?', '?', '?'],
            ['?', '?', '?', '?'],
            ['?', '?', '?', '?'],
            ['?', '?', '?', '?']
        ]
        random.shuffle(dice16)
        die = 0
        for row in range(4):
            for col in range(4):
                self.board[row][col] = dice16[die][random.randint(0,5)]
                die += 1

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