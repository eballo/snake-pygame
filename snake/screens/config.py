from pygame import display, draw
from pygame import event as pygame_event
from pygame import font as pygame_font
from pygame import mixer
from pygame.locals import (
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    K_SPACE,
)

from snake.managers.game_manager import GameManager
from snake.managers.game_state import GameState
from snake.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, RED, WHITE, FPS


class Text:
    @staticmethod
    def draw_text(text, size, color, x, y, screen):
        font = pygame_font.Font("./snake/assets/fonts/RobotoMono-VariableFont_wght.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)


class Config(Text):

    def __init__(self, game_manager: GameManager) -> None:
        self.game_manager = game_manager
        self.selected_option = 0  # 0 = music, 1 = color, 2 = back

    def display(self) -> None:
        clock = self.game_manager.clock
        screen = self.game_manager.screen

        while self.game_manager.state == GameState.GAME_CONFIG:
            clock.tick(FPS)

            for ev in pygame_event.get():
                if ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        self.game_manager.state = GameState.GAME_INTRO

                    elif ev.key == K_UP:
                        self.selected_option = (self.selected_option - 1) % 3
                    elif ev.key == K_DOWN:
                        self.selected_option = (self.selected_option + 1) % 3

                    elif ev.key in (K_LEFT, K_RIGHT):
                        self.handle_left_right(ev.key)

                    elif ev.key in (K_RETURN, K_SPACE):
                        self.handle_enter()

            # --- draw ---
            screen.fill(BLACK)

            self.draw_text(
                "Settings",
                40,
                RED,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 5,
                screen,
            )

            # Option 0: Music
            music_text = f"Music: {'ON' if self.game_manager.music_enabled else 'OFF'}"
            music_color = RED if self.selected_option == 0 else WHITE
            self.draw_text(
                music_text,
                24,
                music_color,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 5 + 80,
                screen,
            )

            # Option 1: Snake color
            color_index = self.game_manager.snake_color_index
            current_color = self.game_manager.snake_colors[color_index]
            color_text = "Snake color (Use LEFT/RIGHT to change)"
            snake_color_text_color = RED if self.selected_option == 1 else WHITE
            self.draw_text(
                color_text,
                24,
                snake_color_text_color,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 5 + 140,
                screen,
            )

            # A simple “preview” rectangle of the snake color
            # (just for visual feedback; optional)
            preview_x = SCREEN_WIDTH / 2 - 40
            preview_y = SCREEN_HEIGHT / 5 + 180

            draw.rect(screen, current_color, (preview_x, preview_y, 80, 20))

            # Option 2: Back
            back_color = RED if self.selected_option == 2 else WHITE
            self.draw_text(
                "Back to main menu",
                24,
                back_color,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 5 + 240,
                screen,
            )

            display.flip()

    def handle_left_right(self, key) -> None:
        # LEFT / RIGHT behavior based on which option is selected
        if self.selected_option == 0:
            # toggle music
            self.game_manager.music_enabled = not self.game_manager.music_enabled
            if not self.game_manager.music_enabled:
                mixer.music.stop()
        elif self.selected_option == 1:
            # cycle snake color
            if key == K_RIGHT:
                self.game_manager.snake_color_index = (
                    self.game_manager.snake_color_index + 1
                ) % len(self.game_manager.snake_colors)
            else:
                self.game_manager.snake_color_index = (
                    self.game_manager.snake_color_index - 1
                ) % len(self.game_manager.snake_colors)

    def handle_enter(self) -> None:
        # ENTER / SPACE pressed
        if self.selected_option == 2:
            self.game_manager.state = GameState.GAME_INTRO
