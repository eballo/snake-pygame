import pygame
import sys

from snake.intro import Intro
from snake.settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT
from snake.food import Food
from snake.snake import Snake


class Game(object):

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", 16)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.running = True
        self.playing = True

    @staticmethod
    def draw_grid(surface):
        for y in range(0, int(GRID_HEIGHT)):
            for x in range(0, int(GRID_WIDTH)):
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                if (x + y) % 2 == 0:
                    color = (93, 216, 228)
                else:
                    color = (84, 194, 205)
                pygame.draw.rect(surface, color, r)

    @staticmethod
    def check_collision(snake, food):
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

    def display_score(self, snake, screen):
        text = self.font.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))

    def gameLoop(self):
        self.draw_grid(self.surface)
        snake = Snake(self)
        food = Food()

        while self.running:
            # Animations
            snake.handle_keys()
            snake.move()
            self.check_collision(snake, food)

            # Visuals
            self.draw_grid(self.surface)
            snake.draw(self.surface)
            food.draw(self.surface)

            self.screen.blit(self.surface, (0, 0))
            self.display_score(snake, self.screen)
            pygame.display.flip()
            self.clock.tick(10)
            # snake.debug_info()

        self.quit()

    def start(self):
        intro = Intro(self)
        # Main file to loop the game
        while self.running:
            # Use the menu state machine
            intro.display_menu()
            # If start is selected, begin the game loop
            while self.playing:
                self.gameLoop()

        self.quit()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
