import pygame

from snake.game_state import GameState
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, RED, GREEN, FPS, WHITE


class Text:

    @staticmethod
    def draw_text(text, size, color, x, y, screen):
        font = pygame.font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)


class Intro(Text):

    def __init__(self, game_manager):
        self.game_manager = game_manager

    # Main Menu Screen
    def display(self):
        if self.game_manager.state.value == GameState.GAME_INTRO.value:
            pygame.mixer.music.load('./snake/assets/music/insertCoin.mp3')
            pygame.mixer.music.play(-1)
            while self.game_manager.state.value == GameState.GAME_INTRO.value:
                self.game_manager.clock.tick(FPS)
                self.game_manager.screen.fill(BLACK)
                self.draw_text("Snake Game", 50, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, self.game_manager.screen)
                self.draw_text("Press SPACE key to play", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_WIDTH / 3 + 100,
                               self.game_manager.screen)
                pygame.display.flip()
                self.game_manager.player_commands.check_events()
            pygame.mixer.music.stop()