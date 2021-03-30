import pygame
import sys

from snake.intro import Intro
from snake.settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_HEIGHT, BOARD_WIDTH, MENU_HEIGHT, GRID_HEIGHT, \
    GRID_WIDTH, BACKGROUND_COLOR_ONE, BACKGROUND_COLOR_TWO, BACKGROUND_COLOR_MENU, FPS, BLACK, WHITE
from snake.food import Food
from snake.snake import Snake, Segment


class Game(object):

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", 16)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.all_sprites = pygame.sprite.Group()
        self.running = True
        self.playing = True

    def draw_grid(self):
        for y in range(0, int(BOARD_HEIGHT), 1):
            for x in range(0, int(BOARD_WIDTH)):
                if (x + y) % 2 == 0:
                    color = BACKGROUND_COLOR_ONE
                else:
                    color = BACKGROUND_COLOR_TWO
                if y < MENU_HEIGHT:
                    color = BACKGROUND_COLOR_MENU
                board = Segment(x * GRID_SIZE, y * GRID_SIZE, color)
                self.all_sprites.add(board)

    @staticmethod
    def check_collision(snake, food):
        if snake.get_head_position().rect == food.rect:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

    def display_score(self, snake, screen):
        text = self.font.render("Score {0}".format(snake.score), 1, WHITE)
        screen.blit(text, (5, 10))

    def gameLoop(self):
        #self.draw_grid()
        snake = Snake(self)
        food = Food()
        self.all_sprites.add(food)

        while self.running:
            # Process Input (events) - Animations
            snake.handle_keys()
            snake.move()
            self.check_collision(snake, food)

            # Update - Visuals
            self.all_sprites.update()

            # Draw - Render
            self.screen.fill(BLACK)
            # self.screen.blit(self.surface, (0, 0))
            self.all_sprites.draw(self.screen)
            self.display_score(snake, self.screen)
            pygame.display.flip()

            # keep the game loop running at the right speed
            self.clock.tick(FPS)

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

    @staticmethod
    def debug():
        print(f"MENU_HEIGHT  : {MENU_HEIGHT}")
        print(f"BOARD_HEIGHT : {BOARD_HEIGHT}")
        print(f"BOARD_WIDTH  : {BOARD_WIDTH}")
        print(f"SCREEN_HEIGHT: {SCREEN_HEIGHT}")
        print(f"SCREEN_WIDTH : {SCREEN_WIDTH}")
        print(f"GRID_HEIGHT  : {GRID_HEIGHT}")
        print(f"GRID_WIDTH   : {GRID_WIDTH}")
