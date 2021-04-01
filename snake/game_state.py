from enum import Enum


class GameState(Enum):
    QUIT = 0
    RUNNING = 1
    GAME_INTRO = 2
    NEW_GAME = 3
    GAME_OVER = 4
    GAME_VICTORY = 5
