import pygame
import sys
import random


class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((Game.SCREEN_WIDTH / 2), (Game.SCREEN_HEIGHT / 2))]
        self.direction = random.choice([Game.UP, Game.DOWN, Game.LEFT, Game.RIGHT])
        self.color = (17, 24, 47)
        self.score = 0

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
        new_pos = (((current_pos[0] + (x * Game.GRID_SIZE)) % Game.SCREEN_WIDTH),
                   ((current_pos[1] + (y * Game.GRID_SIZE)) % Game.SCREEN_HEIGHT))
        if len(self.positions) > 2 and new_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.score = 0
        self.positions = [((Game.SCREEN_WIDTH / 2), (Game.SCREEN_HEIGHT / 2))]
        self.direction = random.choice([Game.UP, Game.DOWN, Game.LEFT, Game.RIGHT])

    def draw(self, surface):
        for pos in self.positions:
            r = pygame.Rect((pos[0], pos[1]), (Game.GRID_SIZE, Game.GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(Game.UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(Game.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(Game.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(Game.RIGHT)


class SnakeAI(Snake):

    def handle_keys(self):
        pass


class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, int(Game.GRID_WIDTH) - 1) * Game.GRID_SIZE,
                         random.randint(0, int(Game.GRID_HEIGHT) - 1) * Game.GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (Game.GRID_SIZE, Game.GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)


class Game(object):
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 480

    GRID_SIZE = 20
    GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
    GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    RUNNING = True
    bg_color = pygame.Color('grey12')

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.Font("./assets/fonts/RobotoMono-VariableFont_wght.ttf", 16)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)

        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()

    def draw_grid(self, surface):
        for y in range(0, int(self.GRID_HEIGHT)):
            for x in range(0, int(self.GRID_WIDTH)):
                r = pygame.Rect((x * Game.GRID_SIZE, y * Game.GRID_SIZE), (Game.GRID_SIZE, Game.GRID_SIZE))
                if (x + y) % 2 == 0:
                    color = (93, 216, 228)
                else:
                    color =(84, 194, 205)
                pygame.draw.rect(surface, color, r)

    @staticmethod
    def check_collision(snake, food):
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

    def display_score(self, snake, screen):
        text = self.my_font.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))

    def play(self):
        self.draw_grid(self.surface)
        snake = Snake()
        food = Food()

        while self.RUNNING:
            # Animations
            snake.handle_keys()
            snake.move()
            self.check_collision(snake, food)

            # Visuals
            self.draw_grid(self.surface)
            snake.draw(self.surface)
            food.draw(self.surface)

            self.screen.blit(self.surface, (0, 0))
            self.display_score(snake, self.screen)
            pygame.display.flip()
            self.clock.tick(10)
            # snake.debug_info()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.play()
