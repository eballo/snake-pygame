from json import loads, dumps
from socket import socket, SOCK_DGRAM
from threading import Thread
from typing import Any

from snakeserver.server_manager import ServerManager
from snakeserver.settings import DEFAULT_TIMEOUT, FORMAT, BUFFER_SIZE


class ServerClientHandler(Thread, socket):

    def __init__(
        self,
        ip: str,
        port: int,
        client_ip_address: tuple[str, int],
        player_number: int,
        server_manager: ServerManager,
    ) -> None:
        socket.__init__(self, type=SOCK_DGRAM)
        Thread.__init__(self, name=f"Client Handler {player_number}")
        self.settimeout(DEFAULT_TIMEOUT)
        self.bind((ip, port + player_number))
        self.daemon = True
        self.player_number = player_number
        self.client_ip_address = client_ip_address
        self.server_manager = server_manager
        # send the player number when whe create the server client handler
        self._send_player_number()

    def _send_player_number(self) -> None:
        message = str(self.player_number).encode(FORMAT)
        self.sendto(message, self.client_ip_address)

    def receive_client_update(self) -> dict | None:
        try:
            data, _ = self.recvfrom(BUFFER_SIZE)
        except TimeoutError:
            print(f"Client {self.player_number} timed out")
            return None
        if data:
            return loads(data.decode(FORMAT))
        return None

    def run(self) -> None:
        while True:
            self.send_other_players_updates()
            response = self.receive_client_update()
            self.update_player_with_client_command(response)
            # self.server_manager.debug()

    def update_player_with_client_command(self, response: dict[str, Any] | None) -> None:
        if response:
            self.server_manager.players[self.player_number - 1] = response

    def join(self, timeout: float | None = None):
        super().join(timeout=timeout if timeout else DEFAULT_TIMEOUT)
        self.close()

    def send_other_players_updates(self) -> None:
        other_players = self.server_manager.players[:]
        del other_players[self.player_number - 1]
        response_json = dumps(other_players)
        # print("other players :" + response_json)
        message = response_json.encode(FORMAT)
        # print(f'message:{message}, address: {self.client_ip_address}')
        self.sendto(message, self.client_ip_address)
