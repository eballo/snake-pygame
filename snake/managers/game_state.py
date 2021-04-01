from enum import Enum


class GameState(Enum):
    QUIT = 0
    RUNNING = 1
    GAME_INTRO = 2
    GAME_RUNNING = 3
    LEVEL_RUNNING = 4
    LEVEL_FINISHED = 5
    GAME_OVER = 6
    GAME_VICTORY = 7
