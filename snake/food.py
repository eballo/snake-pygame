import random

import pygame

from snake.settings import GRID_WIDTH, GRID_SIZE, GRID_HEIGHT, MENU_HEIGHT, FOOD_COLOR


class Food(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(FOOD_COLOR)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.x = random.randint(0, int(GRID_WIDTH) - 1) * GRID_SIZE
        self.rect.y = random.randint(MENU_HEIGHT, int(GRID_HEIGHT) - 1) * GRID_SIZE
