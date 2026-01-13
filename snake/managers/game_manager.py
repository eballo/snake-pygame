import pygame
from pygame import font, time, display, RESIZABLE, HWSURFACE, DOUBLEBUF, sprite, Surface, mixer
from pygame.sprite import Group

from snake.managers.game_state import GameState
from snake.managers.level_manager import LevelManager
from snake.managers.player_commands import PlayerCommands
from snake.models.food import Food
from snake.models.snake import Snake
from snake.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    MENU_HEIGHT,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    GRID_HEIGHT,
    GRID_WIDTH,
    FPS,
    BLACK,
    GREEN,
    YELLOW,
    BLUE,
)


class GameManager:

    def __init__(self, multiplayer: bool = False) -> None:
        self.font = font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", 16)
        self.clock = time.Clock()
        self.screen = display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE | HWSURFACE | DOUBLEBUF
        )
        self.surface = Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.snake_sprites: Group = sprite.Group()
        self.other_players_sprites: Group = sprite.Group()
        self.food_sprites: Group = sprite.Group()
        self.state = GameState.GAME_INTRO
        self.current_level = 0

        # Configuration Settings
        self.music_enabled: bool = False
        self.snake_color_index: int = 0
        self.snake_colors: list[tuple[int, int, int]] = [GREEN, BLUE, WHITE, YELLOW]

        self.player = Snake(self)
        self.players: list[Snake] = []
        self.food: Food = Food(self)
        self.food_sprites.add(self.food)

        self.full_screen = False
        self.multiplayer = multiplayer
        self.stage_name = None
        self.stage_points = None
        self.player_commands = PlayerCommands(self)
        self.level_manager = LevelManager()

    def reset(self) -> None:
        self.current_level = 0
        self.snake_sprites.empty()
        self.food_sprites.empty()
        self.player.reset()
        self.food = Food(self)
        self.food_sprites.add(self.food)

    def soft_reset(self) -> None:
        self.snake_sprites.empty()
        self.food_sprites.empty()
        self.player.soft_reset()
        self.food = Food(self)
        self.food_sprites.add(self.food)

    def process_input(self) -> None:
        self.player_commands.check_events(self.player)
        self.player.move()
        hits = sprite.groupcollide(self.food_sprites, self.snake_sprites, False, False)
        if len(hits) > 0:
            for _ in hits:
                self.eat_food(self.player, self.food)
                mixer.Channel(0).play(mixer.Sound("./snake/assets/music/item.wav"), maxtime=600)

    @staticmethod
    def eat_food(snake: Snake, food: Food) -> None:
        snake.length += 1
        snake.score += 1
        food.randomize_position()

    def display_score(self) -> None:
        text = self.font.render("Score {0}".format(self.player.score), True, WHITE)
        self.screen.blit(text, (5, 10))

    def display_lives(self) -> None:
        text = self.font.render("Lives {0}".format(self.player.lives), True, WHITE)
        self.screen.blit(text, (200, 10))

    def display_stage(self) -> None:
        text = self.font.render(self.stage_name, True, WHITE)
        self.screen.blit(text, (650, 10))

    def debug(self) -> None:
        print(f"MENU_HEIGHT  : {MENU_HEIGHT}")
        print(f"BOARD_HEIGHT : {BOARD_HEIGHT}")
        print(f"BOARD_WIDTH  : {BOARD_WIDTH}")
        print(f"SCREEN_HEIGHT: {SCREEN_HEIGHT}")
        print(f"SCREEN_WIDTH : {SCREEN_WIDTH}")
        print(f"GRID_HEIGHT  : {GRID_HEIGHT}")
        print(f"GRID_WIDTH   : {GRID_WIDTH}")
        print("----")
        print(f"state : {self.state}")

    def validate(self) -> None:
        if self.player.lives == 0:
            self.state = GameState.GAME_OVER
        if self.player.score == self.stage_points:
            self.state = GameState.GAME_RUNNING

    def start_game(self) -> None:
        if self.state.value == GameState.GAME_RUNNING.value:
            self.reset()
            while self.state.value == GameState.GAME_RUNNING.value:
                self.create_world()
                self.game_loop()

    def game_loop(self) -> None:
        if self.state.value == GameState.LEVEL_RUNNING.value:
            if self.music_enabled:
                mixer.music.play(-1)
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
                display.flip()

            if self.music_enabled:
                mixer.music.stop()
            self.current_level += 1

    def create_world(self) -> None:
        if self.state.value == GameState.GAME_RUNNING.value:
            level = self.level_manager.get_level(self.current_level)
            if not level:
                self.state = GameState.GAME_VICTORY
            else:
                mixer.music.load("./snake/assets/music/" + level["music"])
                self.stage_points = level["points"]
                self.stage_name = level["name"]
                self.state = GameState.LEVEL_RUNNING

    @staticmethod
    def toggle_music():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
