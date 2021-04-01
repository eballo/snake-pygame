import pygame

from snake.managers.level_manager import LevelManager
from snake.models.food import Food
from snake.managers.game_state import GameState
from snake.managers.player_commands import PlayerCommands
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, MENU_HEIGHT, BOARD_HEIGHT, BOARD_WIDTH, GRID_HEIGHT, \
    GRID_WIDTH, FPS, BLACK
from snake.models.snake import Snake


class GameManager:

    def __init__(self, multiplayer=False):
        self.font = pygame.font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", 16)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.snake_sprites = pygame.sprite.Group()
        self.food_sprites = pygame.sprite.Group()
        self.state = GameState.GAME_INTRO
        self.current_level = 0
        self.player = Snake(self)
        self.food = Food(self)
        self.food_sprites.add(self.food)

        self.full_screen = False
        self.multiplayer = multiplayer
        self.stage_name = None
        self.stage_points = None
        self.player_commands = PlayerCommands(self)
        self.level_manager = LevelManager()

    def reset(self):
        self.current_level = 0
        self.snake_sprites.empty()
        self.food_sprites.empty()
        self.player.reset()
        self.food = Food(self)
        self.food_sprites.add(self.food)

    def soft_reset(self):
        self.snake_sprites.empty()
        self.food_sprites.empty()
        self.player.soft_reset()
        self.food = Food(self)
        self.food_sprites.add(self.food)

    def process_input(self):
        self.player_commands.check_events(self.player)
        self.player.move()
        hits = pygame.sprite.groupcollide(self.food_sprites, self.snake_sprites, False, False)
        if len(hits) > 0:
            for hit in hits:
                self.eat_food(self.player, self.food)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('./snake/assets/music/item.wav'), maxtime=600)

    @staticmethod
    def eat_food(snake, food):
        snake.length += 1
        snake.score += 1
        food.randomize_position()

    def display_score(self):
        text = self.font.render("Score {0}".format(self.player.score), True, WHITE)
        self.screen.blit(text, (5, 10))

    def display_lives(self):
        text = self.font.render("Lives {0}".format(self.player.lives), True, WHITE)
        self.screen.blit(text, (200, 10))

    def display_stage(self):
        text = self.font.render(self.stage_name, True, WHITE)
        self.screen.blit(text, (650, 10))

    def debug(self):
        print(f"MENU_HEIGHT  : {MENU_HEIGHT}")
        print(f"BOARD_HEIGHT : {BOARD_HEIGHT}")
        print(f"BOARD_WIDTH  : {BOARD_WIDTH}")
        print(f"SCREEN_HEIGHT: {SCREEN_HEIGHT}")
        print(f"SCREEN_WIDTH : {SCREEN_WIDTH}")
        print(f"GRID_HEIGHT  : {GRID_HEIGHT}")
        print(f"GRID_WIDTH   : {GRID_WIDTH}")
        print("----")
        print(f"state : {self.state}")

    def validate(self):
        if self.player.lives == 0:
            self.state = GameState.GAME_OVER
        if self.player.score == self.stage_points:
            self.state = GameState.GAME_RUNNING

    def start_game(self):
        if self.state.value == GameState.GAME_RUNNING.value:
            self.reset()
            while self.state.value == GameState.GAME_RUNNING.value:
                self.create_world()
                self.game_loop()

    def game_loop(self):
        if self.state.value == GameState.LEVEL_RUNNING.value:
            pygame.mixer.music.play(-1)
            while self.state.value == GameState.LEVEL_RUNNING.value:
                # keep the game loop running at the right speed
                self.clock.tick(FPS)

                # Process Input (events) - Animations
                self.process_input()
                self.validate()

                # Update - Visuals
                self.snake_sprites.update()
                self.food_sprites.update()

                # Draw - Render
                self.screen.fill(BLACK)
                self.snake_sprites.draw(self.screen)
                self.food_sprites.draw(self.screen)
                self.display_score()
                self.display_lives()
                self.display_stage()
                pygame.display.flip()
            pygame.mixer.music.stop()
            self.current_level += 1

    def create_world(self):
        if self.state.value == GameState.GAME_RUNNING.value:
            level = self.level_manager.get_level(self.current_level)
            if not level:
                self.state = GameState.GAME_VICTORY
            else:
                pygame.mixer.music.load("./snake/assets/music/" + level["music"])
                self.stage_points = level["points"]
                self.stage_name = level["name"]
                self.state = GameState.LEVEL_RUNNING
