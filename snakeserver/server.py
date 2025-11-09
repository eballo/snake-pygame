from socket import socket, SOCK_DGRAM, AF_INET, SOCK_STREAM
from threading import Thread

from snakeserver.ServerClientHandler import ServerClientHandler
from snakeserver.server_manager import ServerManager
from snakeserver.settings import (
    DEFAULT_PORT,
    FORMAT,
    DEFAULT_IP_SERVER,
    BUFFER_SIZE,
    COMMAND_CLIENT_CONNECT,
)


class SnakeServer(Thread, socket):

    def __init__(self, ip: str | None = None, port: int | None = None) -> None:
        Thread.__init__(self, name="Snake Server thread")
        socket.__init__(self, type=SOCK_DGRAM)
        self.server = socket(AF_INET, SOCK_STREAM)
        self.port = DEFAULT_PORT if port is None else port
        self.ip = DEFAULT_IP_SERVER if ip is None else ip
        self.bind((self.ip, self.port))
        self.server_manager = ServerManager()

    def run(self) -> None:
        print(f"[SERVER HOST IP] {self.getsockname()}  ")
        print("[STARTING] Snake Server is Starting... ")

        for i in range(2):
            player_number = i + 1

            print(f"Waiting for client #{player_number}")
            client_ip_address = self.wait_for_client()

            if client_ip_address:
                print(f"Sending player number {player_number} to {client_ip_address}")
                self.create_player_handler(client_ip_address, player_number)

        print("[STARTING] Snake game is starting...")
        # keep the main thread alive
        while True:
            pass

    def wait_for_client(self) -> tuple[str, int] | None:
        data, address_info = self.recvfrom(BUFFER_SIZE)
        print(f"Data:{data!r}, Address Info: {address_info}")

        if data:
            decoded_data = data.decode(FORMAT)
            if decoded_data != COMMAND_CLIENT_CONNECT:
                raise ValueError(f"Expecting {COMMAND_CLIENT_CONNECT}, but got {decoded_data}")
            print(f"[CONNECTED] Client {address_info} connected successfully")
            return address_info
        return None

    def create_player_handler(self, client_ip_address: tuple[str, int], player_number: int) -> None:
        print(f"Create player Handler for {player_number}")
        client_handler = ServerClientHandler(
            self.ip, self.port, client_ip_address, player_number, self.server_manager
        )
        self.server_manager.clients.append(client_handler)
        client_handler.start()

    def join(self, timeout: float | None = None) -> None:
        try:
            super().join(timeout)
        finally:
            self.close()


if __name__ == "__main__":
    print("[STARTING] Snake Server is starting ...")
    server = SnakeServer()
    server.start()
