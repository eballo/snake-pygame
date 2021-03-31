import pygame

from snake.intro import Text
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, BLACK, FPS, YELLOW


class Victory(Text):

    def __init__(self, game_manager):
        self.game_manager = game_manager

    # Main Menu Screen
    def display(self):
        pygame.mixer.music.load('./snake/assets/music/victory.mp3')
        pygame.mixer.music.play(-1)
        while self.game_manager.victory:
            self.game_manager.clock.tick(FPS)
            self.game_manager.screen.fill(BLACK)
            self.draw_text("Victory!!", 50, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, self.game_manager.screen)
            self.draw_text("Score : " + str(self.game_manager.snake.score), 30, GREEN, SCREEN_WIDTH / 2,
                           SCREEN_HEIGHT / 3 + 100, self.game_manager.screen)
            pygame.display.flip()
            self.check_events()
        pygame.mixer.music.stop()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_manager.run_display = False
                self.game_manager.running = False
                self.game_manager.game_running = False
                self.game_manager.game_over = False
                self.game_manager.victory = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_manager.run_display = False
                    self.game_manager.running = False
                    self.game_manager.game_running = False
                    self.game_manager.game_over = False
                    self.game_manager.victory = False
                if event.key == pygame.K_SPACE:
                    self.game_manager.run_display = True
                    self.game_manager.running = True
                    self.game_manager.game_running = False
                    self.game_manager.game_over = False
                    self.game_manager.victory = False
