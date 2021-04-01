import json
import os

import pygame

from snake.managers.game_state import GameState
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, LEFT, UP, RIGHT, DOWN


class PlayerCommands:

    def __init__(self, game_manager):
        self.joysticks = []
        self.button_keys = None
        # 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
        # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
        self.analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
        self.initialize_controllers()
        self.game_manager = game_manager

    def initialize_controllers(self):
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))

        for joystick in self.joysticks:
            joystick.init()

        with open(os.path.join("./snake/assets/controllers/ps4.json"), 'r+') as file:
            self.button_keys = json.load(file)

    def check_events(self, player=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                print("key pressed")
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
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
                        self.game_manager.full_screen = True
                    else:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                                pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF)
                        self.game_manager.full_screen = False
                if self.game_manager.state == GameState.GAME_RUNNING or \
                        self.game_manager.state == GameState.LEVEL_RUNNING:
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
                if self.game_manager.state == GameState.GAME_RUNNING or \
                        self.game_manager.state == GameState.LEVEL_RUNNING:
                    if event.button == self.button_keys['left_arrow']:
                        player.turn(LEFT)
                    if event.button == self.button_keys['right_arrow']:
                        player.turn(RIGHT)
                    if event.button == self.button_keys['down_arrow']:
                        player.turn(DOWN)
                    if event.button == self.button_keys['up_arrow']:
                        player.turn(UP)
            if event.type == pygame.JOYAXISMOTION:
                if self.game_manager.state == GameState.GAME_RUNNING or \
                        self.game_manager.state == GameState.LEVEL_RUNNING:
                    self.analog_keys[event.axis] = event.value
                    if abs(self.analog_keys[0]) > .4:
                        if self.analog_keys[0] < -.7:
                            player.turn(LEFT)
                        if self.analog_keys[0] > .7:
                            player.turn(RIGHT)
                    # Vertical Analog
                    if abs(self.analog_keys[1]) > .4:
                        if self.analog_keys[1] < -.7:
                            player.turn(UP)
                        if self.analog_keys[1] > .7:
                            player.turn(DOWN)

    def quit(self):
        if self.game_manager.state == GameState.GAME_RUNNING or self.game_manager.state == GameState.LEVEL_RUNNING:
            self.game_manager.state = GameState.GAME_INTRO
        else:
            self.game_manager.state = GameState.QUIT

    def new_game(self):
        self.game_manager.state = GameState.GAME_RUNNING

    def intro(self):
        self.game_manager.state = GameState.GAME_INTRO
