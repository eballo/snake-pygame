import pygame

from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Intro:

    def __init__(self, game):
        self.intro_font = pygame.font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", 40)
        self.game = game
        self.run_display = True

    def draw_text(self, text, size, color, x, y):
        text_surface = self.intro_font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.surface.blit(text_surface, text_rect)

    def blit_screen(self):
        self.game.screen.blit(pygame.transform.scale(self.game.surface, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        pygame.display.update()

    # Main Menu Screen
    def display_menu(self):
        while self.run_display:
            self.draw_text("Snake Game", 100, (255, 0, 0), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            self.blit_screen()
            self.check_events()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_display = False
                self.game.playing = False
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run_display = False
                    self.game.playing = False
                    self.game.running = False
                if event.key == pygame.K_SPACE:
                    self.run_display = False
                    self.game.running = True
                    self.game.playing = True

