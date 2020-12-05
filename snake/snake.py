import random

import pygame

from snake.client import Client
from snake.settings import UP, DOWN, LEFT, RIGHT, GRID_SIZE, BOARD_WIDTH, BOARD_HEIGHT, SNAKE_COLOR, \
    BACKGROUND_COLOR_ONE, MENU_HEIGHT, GRID_HEIGHT, SCREEN_HEIGHT


class Snake(object):
    def __init__(self, game):
        self.game = game
        self.length = 3
        self.score = 0
        self.positions = [((BOARD_WIDTH // 2), (BOARD_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = SNAKE_COLOR
        self.client = Client()

    def debug_info(self):
        print("----")
        print(f"position: {self.positions}")
        print(f"direction: {self.direction}")
        print(f"length: {self.length}")

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] - 1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        current_pos = self.get_head_position()
        x, y = self.direction
        new_x = ((current_pos[0] + (x * GRID_SIZE)) % BOARD_WIDTH)
        new_y = (current_pos[1] + (y * GRID_SIZE))
        if new_y >= SCREEN_HEIGHT:
            new_y = MENU_HEIGHT * GRID_HEIGHT
        if new_y < (MENU_HEIGHT -1) * GRID_HEIGHT:
            new_y = SCREEN_HEIGHT
        new_pos = (new_x, new_y)
        if len(self.positions) > 2 and new_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 3
        self.score = 0
        self.positions = [((BOARD_WIDTH // 2), (BOARD_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for pos in self.positions:
            r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BACKGROUND_COLOR_ONE, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.playing = False
                    self.game.running = False
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

    def send(self):
        positions = ', '.join(map(str, self.positions))
        self.client.send(positions)
