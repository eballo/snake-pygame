import pygame

from snake.managers.game_state import GameState
from snake.screens.intro import Text
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, BLACK, FPS


class GameOver(Text):

    def __init__(self, game_manager):
        self.game_manager = game_manager

    # Main Menu Screen
    def display(self):
        if self.game_manager.state.value == GameState.GAME_OVER.value:
            pygame.mixer.music.load('./snake/assets/music/dead.mp3')
            pygame.mixer.music.play(-1)
            while self.game_manager.state.value == GameState.GAME_OVER.value:
                self.game_manager.clock.tick(FPS)
                self.game_manager.screen.fill(BLACK)
                self.draw_text("GAME OVER", 50, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, self.game_manager.screen)
                self.draw_text("Score : " + str(self.game_manager.player.score), 30, GREEN, SCREEN_WIDTH / 2,
                               SCREEN_HEIGHT / 3 + 100, self.game_manager.screen)
                pygame.display.flip()
                self.game_manager.player_commands.check_events()
            pygame.mixer.music.stop()