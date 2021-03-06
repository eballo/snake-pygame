import json
import random

import pygame

from snake.settings import UP, DOWN, LEFT, RIGHT, GRID_SIZE, BOARD_WIDTH, BOARD_HEIGHT, SNAKE_COLOR, \
    MENU_HEIGHT, GRID_HEIGHT, SCREEN_HEIGHT


class Segment(pygame.sprite.Sprite):

    def __init__(self, x, y, color=SNAKE_COLOR):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Snake:

    def __init__(self, game_manager, color=SNAKE_COLOR):
        self.game_manager = game_manager
        self.color = color
        self.length = 3
        self.score = 0
        self.lives = 1
        self.positions = [Segment((BOARD_WIDTH // 2), (BOARD_HEIGHT // 2), color)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        current_pos = self.get_head_position()
        x, y = self.direction
        new_x = ((current_pos.rect.x + (x * GRID_SIZE)) % BOARD_WIDTH)
        new_y = (current_pos.rect.y + (y * GRID_SIZE))
        if new_y >= SCREEN_HEIGHT:
            new_y = MENU_HEIGHT * GRID_HEIGHT
        if new_y < (MENU_HEIGHT - 1) * GRID_HEIGHT:
            new_y = SCREEN_HEIGHT
        new_segment = Segment(new_x, new_y)
        # check new segment collision with the body
        sub_group = pygame.sprite.Group()
        for seg in self.positions[2:]:
            sub_group.add(seg)
        hit = pygame.sprite.spritecollide(new_segment, sub_group, False)
        if len(self.positions) > 2 and len(hit) > 0:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('./snake/assets/music/dead.mp3'))
            self.lives -= 1
            self.game_manager.soft_reset()
        else:
            self.positions.insert(0, new_segment)
            self.game_manager.snake_sprites.add(new_segment)
            if len(self.positions) > self.length:
                old_segment = self.positions.pop()
                self.game_manager.snake_sprites.remove(old_segment)

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * - 1) == self.direction:
            return
        else:
            self.direction = point

    def reset(self):
        self.length = 3
        self.lives = 1
        self.score = 0
        segment = Segment((BOARD_WIDTH // 2), (BOARD_HEIGHT // 2))
        self.positions = [segment]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.game_manager.snake_sprites.add(segment)

    def soft_reset(self):
        segment = Segment((BOARD_WIDTH // 2), (BOARD_HEIGHT // 2))
        self.positions = [segment]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.game_manager.snake_sprites.add(segment)

    def get_json(self):
        segments = []
        for pos in self.positions:
            segments.append((pos.rect.x, pos.rect.y))
        data = {"direction": self.direction, "positions": segments, "color": self.color, "length": self.length,
                "lives": self.lives}
        return json.dumps(data)

    def update_from_json(self, json_response):
        snake = Snake(self.game_manager)
        segments = []
        for pos in json_response["positions"]:
            segments.append(Segment(pos[0], pos[1], json_response["color"]))

        snake.color = json_response["color"]
        snake.direction = json_response["direction"]
        snake.positions = segments
        snake.length = json_response["length"]
        snake.lives = json_response["lives"]
        return snake

    def debug_info(self):
        print("----")
        print(f"position: {self.positions}")
        print(f"direction: {self.direction}")
        print(f"length: {self.length}")
        print(f"score: {self.score}")
        print(f"lives: {self.lives}")
        print(f"color: {self.color}")
