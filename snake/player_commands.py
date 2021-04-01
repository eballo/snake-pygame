import json
import os

import pygame

from snake.game_state import GameState


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

    def check_events(self):
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
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == self.button_keys["circle"]:
                    self.quit()
                if event.button == self.button_keys["x"]:
                    self.new_game()

    def quit(self):
        self.game_manager.state = GameState.QUIT

    def new_game(self):
        self.game_manager.state = GameState.NEW_GAME

    def intro(self):
        self.game_manager.state = GameState.GAME_INTRO
