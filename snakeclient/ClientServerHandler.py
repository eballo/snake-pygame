from json import loads
from socket import socket, SOCK_DGRAM
from threading import Thread

from snake.managers.game_manager import GameManager
from snakeserver.settings import DEFAULT_TIMEOUT, COMMAND_CLIENT_CONNECT, FORMAT, BUFFER_SIZE


class ClientServerHandler(socket, Thread):

    def __init__(
        self,
        bind_address: tuple[str, int],
        server_address: tuple[str, int],
        game_manager: GameManager,
    ) -> None:
        socket.__init__(self, type=SOCK_DGRAM)
        Thread.__init__(self)
        self.settimeout(DEFAULT_TIMEOUT)
        self.daemon = True
        self.bind(bind_address)
        self.server_address = server_address
        self.player_number = -1
        self.game_manager = game_manager

    def run(self) -> None:
        self._handshake_with_server()
        self.player_number = self.receive_player_number()
        print(f"player number: {self.player_number}")

        while True:
            self.receive_other_players_updates_json()
            self.send_client_update(self.game_manager.player.get_json())

    def __del__(self) -> None:
        self.close()

    def _handshake_with_server(self) -> None:
        message = COMMAND_CLIENT_CONNECT.encode(FORMAT)
        print(f"message:{message!r}, address: {self.server_address}")
        self.sendto(message, self.server_address)
        return None

    def receive_player_number(self) -> int:
        data, address = self.recvfrom(BUFFER_SIZE)
        if data is None:
            return -1
        decoded = data.decode(FORMAT)
        player_number = int(decoded)
        print("player_number", player_number)

        # OVERWRITE self.server_address to the one received, since that will be address of the client handler
        self.server_address = address
        return player_number

    def receive_other_players_updates_json(self) -> None:
        data, address = self.recvfrom(BUFFER_SIZE)
        if data is None:
            raise ValueError("Unable to receive game update!")
        decoded = data.decode(FORMAT)
        other_players_json = loads(decoded)

        self.game_manager.other_players_sprites.empty()
        for player in other_players_json:
            snake = self.game_manager.player.update_from_json(player)
            self.game_manager.players.append(snake)
            for seg in snake.positions:
                self.game_manager.other_players_sprites.add(seg)

    def send_client_update(self, text: str) -> None:
        message = text.encode(FORMAT)
        # print(f'message:{message}, address: {self.server_address}')
        self.sendto(message, self.server_address)
