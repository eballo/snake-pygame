import pygame

from snake.game_state import GameState
from snake.intro import Text
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, BLACK, FPS, YELLOW


class Victory(Text):

    def __init__(self, game_manager):
        self.game_manager = game_manager

    # Main Menu Screen
    def display(self):
        if self.game_manager.state.value == GameState.GAME_VICTORY.value:
            pygame.mixer.music.load('./snake/assets/music/victory.mp3')
            pygame.mixer.music.play(-1)
            while self.game_manager.state.value == GameState.GAME_VICTORY.value:
                self.game_manager.clock.tick(FPS)
                self.game_manager.screen.fill(BLACK)
                self.draw_text("Victory!!", 50, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, self.game_manager.screen)
                self.draw_text("Score : " + str(self.game_manager.snake.score), 30, GREEN, SCREEN_WIDTH / 2,
                               SCREEN_HEIGHT / 3 + 100, self.game_manager.screen)
                pygame.display.flip()
                self.game_manager.player_commands.check_events()
            pygame.mixer.music.stop()

