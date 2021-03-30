import pygame
import sys

from snake.game_manager import GameManager
from snake.intro import Intro
from snake.settings import FPS, BLACK


class Game(object):

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.game_manager = GameManager()

    def game_loop(self):
        while self.game_manager.running:
            # keep the game loop running at the right speed
            self.game_manager.clock.tick(FPS)

            # Process Input (events) - Animations
            self.game_manager.process_input()

            # Update - Visuals
            self.game_manager.snake_sprites.update()

            # Draw - Render
            self.game_manager.screen.fill(BLACK)
            self.game_manager.snake_sprites.draw(self.game_manager.screen)
            self.game_manager.display_score()
            pygame.display.flip()

        self.quit()

    def start(self):
        intro = Intro(self.game_manager)
        # Main file to loop the game
        while self.game_manager.running:
            # Use the menu state machine
            intro.display_menu()
            # If start is selected, begin the game loop
            while self.game_manager.playing:
                self.game_loop()
        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
