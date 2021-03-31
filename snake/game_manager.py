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
        self.run_display = True
        self.running = True
        self.game_running = True
        self.game_over = False

        self.snake = Snake(self)
        self.food = Food(self)
        self.food_sprites.add(self.food)

    def reset(self):
        self.snake_sprites.empty()
        self.food_sprites.empty()
        self.snake.reset()
        self.food = Food(self)
        self.food_sprites.add(self.food)

    def soft_reset(self):
        self.snake_sprites.empty()
        self.food_sprites.empty()
        self.snake.soft_reset()
        self.food = Food(self)
        self.food_sprites.add(self.food)

    def process_input(self):
        self.snake.handle_keys()
        self.snake.move()
        hits = pygame.sprite.groupcollide(self.food_sprites, self.snake_sprites, False, False)
        if len(hits) > 0:
            for hit in hits:
                self.eat_food(self.snake, self.food)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./snake/assets/music/item.wav'), maxtime=600)

    @staticmethod
    def eat_food(snake, food):
        snake.length += 1
        snake.score += 1
        food.randomize_position()

    def display_score(self):
        text = self.font.render("Score {0}".format(self.snake.score), 1, WHITE)
        self.screen.blit(text, (5, 10))

    def display_lives(self):
        text = self.font.render("Lives {0}".format(self.snake.lives), 1, WHITE)
        self.screen.blit(text, (200, 10))

    def debug(self):
        print(f"MENU_HEIGHT  : {MENU_HEIGHT}")
        print(f"BOARD_HEIGHT : {BOARD_HEIGHT}")
        print(f"BOARD_WIDTH  : {BOARD_WIDTH}")
        print(f"SCREEN_HEIGHT: {SCREEN_HEIGHT}")
        print(f"SCREEN_WIDTH : {SCREEN_WIDTH}")
        print(f"GRID_HEIGHT  : {GRID_HEIGHT}")
        print(f"GRID_WIDTH   : {GRID_WIDTH}")
        print("----")
        print(f"run_display : {self.run_display}")
        print(f"game_running : {self.game_running}")
        print(f"running : {self.running}")
        print(f"game_running : {self.game_running}")

    def validate(self):
        if self.snake.lives == 0:
            self.game_running = False
            self.run_display = True
            self.game_over = True
