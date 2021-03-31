import pygame
import sys

from snake.game_manager import GameManager
from snake.game_over import GameOver
from snake.intro import Intro
from snake.settings import FPS, BLACK


class Game(object):

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Snake!")
        self.game_manager = GameManager()

    def game_loop(self):
        while self.game_manager.game_running:
            # keep the game loop running at the right speed
            self.game_manager.clock.tick(FPS)

            # Process Input (events) - Animations
            self.game_manager.process_input()

            if self.game_manager.snake.lives == 0:
                self.game_manager.game_running = False
                self.game_manager.run_display = True
                self.game_manager.game_over = True
                break

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

    def start(self):
        intro = Intro(self.game_manager)
        game_over = GameOver(self.game_manager)
        # Main file to loop the game
        while self.game_manager.running:
            # Use the menu state machine
            intro.display_intro()
            self.game_loop()
            game_over.display_game_over()
        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
