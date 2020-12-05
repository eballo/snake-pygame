import pygame
import sys

from snake.intro import Intro
from snake.settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_HEIGHT, BOARD_WIDTH, MENU_HEIGHT, GRID_HEIGHT, \
    GRID_WIDTH, BACKGROUND_COLOR_ONE, BACKGROUND_COLOR_TWO, BACKGROUND_COLOR_MENU, DISCONNECT_MESSAGE
from snake.food import Food
from snake.snake import Snake


class Game(object):

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.snake = Snake(self)
        self.food = Food()
        self.font = pygame.font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", 16)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.running = True
        self.playing = True

    def debug(self):
        print(f"MENU_HEIGHT  : {MENU_HEIGHT}")
        print(f"BOARD_HEIGHT : {BOARD_HEIGHT}")
        print(f"BOARD_WIDTH  : {BOARD_WIDTH}")
        print(f"SCREEN_HEIGHT: {SCREEN_HEIGHT}")
        print(f"SCREEN_WIDTH : {SCREEN_WIDTH}")
        print(f"GRID_HEIGHT  : {GRID_HEIGHT}")
        print(f"GRID_WIDTH   : {GRID_WIDTH}")

    @staticmethod
    def draw_grid(surface):
        for y in range(0, int(BOARD_HEIGHT), 1):
            for x in range(0, int(BOARD_WIDTH)):
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                if (x + y) % 2 == 0:
                    color = BACKGROUND_COLOR_ONE
                else:
                    color = BACKGROUND_COLOR_TWO
                if y < MENU_HEIGHT:
                    color = BACKGROUND_COLOR_MENU
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

        while self.running:
            # Animations
            self.snake.handle_keys()
            self.snake.move()
            self.snake.send()
            self.check_collision(self.snake, self.food)

            # Visuals
            self.draw_grid(self.surface)
            self.snake.draw(self.surface)
            self.food.draw(self.surface)

            self.screen.blit(self.surface, (0, 0))
            self.display_score(self.snake, self.screen)
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

    def quit(self):
        self.snake.send(DISCONNECT_MESSAGE)
        pygame.quit()
        sys.exit()
