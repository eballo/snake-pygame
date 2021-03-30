import pygame

from snake.food import Food
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, MENU_HEIGHT, BOARD_HEIGHT, BOARD_WIDTH, GRID_HEIGHT, \
    GRID_WIDTH
from snake.snake import Snake


class GameManager:

    def __init__(self):
        self.font = pygame.font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", 16)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.snake_sprites = pygame.sprite.Group()
        self.food_sprites = pygame.sprite.Group()
        self.running = True
        self.playing = True

        self.snake = Snake(self)
        self.food = Food(self)
        self.snake_sprites.add(self.food)

    def reset(self):
        self.snake_sprites.empty()
        self.snake.reset()
        self.food = Food(self)
        self.snake_sprites.add(self.food)

    def process_input(self):
        self.snake.handle_keys()
        self.snake.move()
        hits = pygame.sprite.spritecollide(self.food, self.snake_sprites, False)
        if len(hits) > 1:
            self.check_collision(self.snake, self.food)

    @staticmethod
    def check_collision(snake, food):
        snake.length += 1
        snake.score += 1
        food.randomize_position()

    def display_score(self):
        text = self.font.render("Score {0}".format(self.snake.score), 1, WHITE)
        self.screen.blit(text, (5, 10))

    @staticmethod
    def debug():
        print(f"MENU_HEIGHT  : {MENU_HEIGHT}")
        print(f"BOARD_HEIGHT : {BOARD_HEIGHT}")
        print(f"BOARD_WIDTH  : {BOARD_WIDTH}")
        print(f"SCREEN_HEIGHT: {SCREEN_HEIGHT}")
        print(f"SCREEN_WIDTH : {SCREEN_WIDTH}")
        print(f"GRID_HEIGHT  : {GRID_HEIGHT}")
        print(f"GRID_WIDTH   : {GRID_WIDTH}")
