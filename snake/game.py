import sys

import pygame

from snake.managers.game_manager import GameManager
from snake.screens.game_over import GameOver
from snake.managers.game_state import GameState
from snake.screens.intro import Intro
from snake.screens.victory import Victory


class Game(object):

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.set_caption("Snake!")
        self.game_manager = GameManager()

    def start(self):
        intro = Intro(self.game_manager)
        game_over = GameOver(self.game_manager)
        victory = Victory(self.game_manager)
        # Main file to loop the game
        while self.game_manager.state.value >= GameState.RUNNING.value:
            # Use the menu state machine
            intro.display()
            self.game_manager.start_game()
            victory.display()
            game_over.display()
        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
