import sys

import pygame

from snake.managers.game_manager import GameManager
from snake.screens.game_over import GameOver
from snake.managers.game_state import GameState
from snake.screens.intro import Intro
from snake.settings import FPS, BLACK
from snake.screens.victory import Victory


class Game(object):

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.set_caption("Snake!")
        self.game_manager = GameManager()

    def game_loop(self):
        if self.game_manager.state.value == GameState.NEW_GAME.value:
            pygame.mixer.music.load('./snake/assets/music/creationOfValues.mp3')
            pygame.mixer.music.play(-1)
            self.game_manager.reset()
        while self.game_manager.state.value == GameState.NEW_GAME.value:
            # keep the game loop running at the right speed
            self.game_manager.clock.tick(FPS)

            # Process Input (events) - Animations
            self.game_manager.process_input()
            self.game_manager.validate()

            # Update - Visuals
            self.game_manager.snake_sprites.update()
            self.game_manager.food_sprites.update()

            # Draw - Render
            self.game_manager.screen.fill(BLACK)
            self.game_manager.snake_sprites.draw(self.game_manager.screen)
            self.game_manager.food_sprites.draw(self.game_manager.screen)
            self.game_manager.display_score()
            self.game_manager.display_lives()
            pygame.display.flip()
        pygame.mixer.music.stop()

    def start(self):
        intro = Intro(self.game_manager)
        game_over = GameOver(self.game_manager)
        victory = Victory(self.game_manager)
        # Main file to loop the game
        while self.game_manager.state.value >= GameState.RUNNING.value:
            # Use the menu state machine
            intro.display()
            self.game_loop()
            victory.display()
            game_over.display()
        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
