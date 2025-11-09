from json import load
from os.path import join
from typing import TYPE_CHECKING

import pygame
from pygame.joystick import JoystickType

from snake.managers.game_state import GameState
from snake.models.snake import Snake
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, LEFT, UP, RIGHT, DOWN

if TYPE_CHECKING:
    from snake.managers.game_manager import GameManager


class PlayerCommands:

    def __init__(self, game_manager: "GameManager") -> None:
        self.joysticks: list[JoystickType] = []
        self.button_keys: dict = {}
        # 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
        # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
        self.analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
        self.initialize_controllers()
        self.game_manager = game_manager

    def initialize_controllers(self) -> None:
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))

        for joystick in self.joysticks:
            joystick.init()

        with open(join("./snake/assets/controllers/ps4.json"), "r+") as file:
            self.button_keys = load(file)

    def check_events(self, player: Snake | None = None) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_SPACE:
                    if self.game_manager.state == GameState.GAME_INTRO:
                        self.new_game()
                    elif self.game_manager.state == GameState.GAME_OVER:
                        self.intro()
                    elif self.game_manager.state == GameState.GAME_VICTORY:
                        self.intro()
                if event.key == pygame.K_f:
                    if not self.game_manager.full_screen:
                        pygame.display.set_mode(
                            (SCREEN_WIDTH, SCREEN_HEIGHT),
                            pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF,
                        )
                        self.game_manager.full_screen = True
                    else:
                        pygame.display.set_mode(
                            (SCREEN_WIDTH, SCREEN_HEIGHT),
                            pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF,
                        )
                        self.game_manager.full_screen = False
                if (
                    self.game_manager.state == GameState.GAME_RUNNING
                    or self.game_manager.state == GameState.LEVEL_RUNNING
                ) and player is not None:
                    if event.key == pygame.K_UP:
                        player.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        player.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        player.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        player.turn(RIGHT)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == self.button_keys["circle"]:
                    self.quit()
                if event.button == self.button_keys["x"]:
                    self.new_game()
                if (
                    self.game_manager.state == GameState.GAME_RUNNING
                    or self.game_manager.state == GameState.LEVEL_RUNNING
                ) and player is not None:
                    if event.button == self.button_keys["left_arrow"]:
                        player.turn(LEFT)
                    if event.button == self.button_keys["right_arrow"]:
                        player.turn(RIGHT)
                    if event.button == self.button_keys["down_arrow"]:
                        player.turn(DOWN)
                    if event.button == self.button_keys["up_arrow"]:
                        player.turn(UP)
            if event.type == pygame.JOYAXISMOTION:
                if (
                    self.game_manager.state == GameState.GAME_RUNNING
                    or self.game_manager.state == GameState.LEVEL_RUNNING
                ) and player is not None:
                    self.analog_keys[event.axis] = event.value
                    if abs(self.analog_keys[0]) > 0.4:
                        if self.analog_keys[0] < -0.7:
                            player.turn(LEFT)
                        if self.analog_keys[0] > 0.7:
                            player.turn(RIGHT)
                    # Vertical Analog
                    if abs(self.analog_keys[1]) > 0.4:
                        if self.analog_keys[1] < -0.7:
                            player.turn(UP)
                        if self.analog_keys[1] > 0.7:
                            player.turn(DOWN)

    def quit(self) -> None:
        if (
            self.game_manager.state == GameState.GAME_RUNNING
            or self.game_manager.state == GameState.LEVEL_RUNNING
        ):
            self.game_manager.state = GameState.GAME_INTRO
        else:
            self.game_manager.state = GameState.QUIT

    def new_game(self) -> None:
        self.game_manager.state = GameState.GAME_RUNNING

    def intro(self) -> None:
        self.game_manager.state = GameState.GAME_INTRO
