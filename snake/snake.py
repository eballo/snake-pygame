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

    def __init__(self, game):
        self.game = game
        self.length = 3
        self.score = 0
        self.positions = [Segment((BOARD_WIDTH // 2), (BOARD_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

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
        new_x = ((current_pos.rect.x + (x * GRID_SIZE)) % BOARD_WIDTH)
        new_y = (current_pos.rect.y + (y * GRID_SIZE))
        if new_y >= SCREEN_HEIGHT:
            new_y = MENU_HEIGHT * GRID_HEIGHT
        if new_y < (MENU_HEIGHT - 1) * GRID_HEIGHT:
            new_y = SCREEN_HEIGHT
        new_segment = Segment(new_x, new_y)
        if len(self.positions) > 2 and new_segment in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_segment)
            self.game.all_sprites.add(new_segment)
            if len(self.positions) > self.length:
                old_segment = self.positions.pop()
                self.game.all_sprites.remove(old_segment)

    def reset(self):
        self.length = 3
        self.score = 0
        segment = Segment((BOARD_WIDTH // 2), (BOARD_HEIGHT // 2))
        self.positions = [segment]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.game.all_sprites.empty()
        self.game.all_sprites.add(segment)

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

    def debug_info(self):
        print("----")
        print(f"position: {self.positions}")
        print(f"direction: {self.direction}")
        print(f"length: {self.length}")