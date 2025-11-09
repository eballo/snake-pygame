from sys import exit as quit_app

from pygame import init, mixer, font, display
from pygame import quit as quit_game

from snake.managers.game_manager import GameManager
from snake.managers.game_state import GameState
from snake.screens.game_over import GameOver
from snake.screens.intro import Intro
from snake.screens.victory import Victory


class Game(object):

    def __init__(self):
        init()
        mixer.init()
        font.init()
        display.set_caption("Snake!")
        self.game_manager = GameManager()
        self.intro = Intro(self.game_manager)
        self.game_over = GameOver(self.game_manager)
        self.victory = Victory(self.game_manager)

    def start(self) -> None:
        while self.game_manager.state.value >= GameState.RUNNING.value:
            self.intro.display()
            self.game_manager.start_game()
            self.victory.display()
            self.game_over.display()
        self.quit()

    @staticmethod
    def quit() -> None:
        quit_game()
        quit_app()
