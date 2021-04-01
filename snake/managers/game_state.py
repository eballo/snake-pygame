from enum import Enum


class GameState(Enum):
    QUIT = 0
    RUNNING = 1
    GAME_INTRO = 2
    GAME_RUNNING = 3
    LEVEL_RUNNING = 4
    GAME_OVER = 5
    GAME_VICTORY = 6
