from random import randint
from typing import TYPE_CHECKING

from pygame import Surface, sprite

from snake.settings import GRID_WIDTH, GRID_SIZE, GRID_HEIGHT, MENU_HEIGHT, FOOD_COLOR

if TYPE_CHECKING:
    from snake.managers.game_manager import GameManager


class Food(sprite.Sprite):

    def __init__(self, game_manager: "GameManager") -> None:
        super().__init__()
        self.game_manager = game_manager
        self.image = Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(FOOD_COLOR)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self) -> None:
        self.rect.x = randint(0, int(GRID_WIDTH) - 1) * GRID_SIZE
        self.rect.y = randint(MENU_HEIGHT, int(GRID_HEIGHT) - 1) * GRID_SIZE
