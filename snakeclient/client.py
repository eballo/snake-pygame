import random

import pygame

from snake.managers.game_manager import GameManager
from snake.managers.game_state import GameState
from snake.settings import FPS, BLACK
from snakeclient.ClientServerHandler import ClientServerHandler
from snakeserver.settings import DEFAULT_IP_SERVER, DEFAULT_PORT


class SnakeClient:

    def __init__(self, ip_server=None, port_server=None):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.set_caption("Snake!")
        self.game_manager = GameManager(multiplayer=True)
        self.ip_server = DEFAULT_IP_SERVER if ip_server is None else ip_server
        self.port_server = DEFAULT_PORT if port_server is None else port_server

    def start(self):
        # Randomly generate the address for this client
        local_address = ('localhost', random.randint(10000, 20000))
        server_address = (self.ip_server, self.port_server)

        svh = ClientServerHandler(local_address, server_address)
        svh.start()

        print(f'[START] Client starting...')
        self.game_manager.state = GameState.GAME_RUNNING

        while self.game_manager.state == GameState.GAME_RUNNING:
            # keep the game loop running at the right speed
            self.game_manager.clock.tick(FPS)

            # Process Input (events) - Animations
            self.game_manager.process_input()
            self.game_manager.validate()

            # Update - Visuals
            self.game_manager.snake_sprites.update()
            self.game_manager.food_sprites.update()

            # Draw - Render
            self.game_manager.screen.fill(BLACK)
            self.game_manager.snake_sprites.draw(self.game_manager.screen)
            self.game_manager.food_sprites.draw(self.game_manager.screen)
            self.game_manager.display_score()
            self.game_manager.display_lives()
            self.game_manager.display_stage()
            pygame.display.flip()


if __name__ == '__main__':
    client = SnakeClient()
    client.start()
