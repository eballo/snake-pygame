import random

import pygame

from snake.settings import GRID_WIDTH, GRID_SIZE, GRID_HEIGHT, MENU_HEIGHT


class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (180, 10, 10)
        self.randomize_position()

    def randomize_position(self):
        x = random.randint(0, int(GRID_WIDTH) - 1) * GRID_SIZE
        y = random.randint(MENU_HEIGHT, int(GRID_HEIGHT) - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        # r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        # pygame.draw.rect(surface, self.color, r)
        r = 5
        pygame.draw.circle(surface, self.color, (
        (self.position[0] + int(GRID_WIDTH / 2) - int(r / 2)), (self.position[1] + int(GRID_WIDTH / 2) - int(r / 2))),
                           r)
