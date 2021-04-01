from threading import Thread
from socket import socket, SOCK_DGRAM
from snakeserver.settings import DEFAULT_TIMEOUT, FORMAT, BUFFER_SIZE


class ServerClientHandler(Thread, socket):

    def __init__(self, ip, port, client_ip_address, player_number, server_manager):
        socket.__init__(self, type=SOCK_DGRAM)
        Thread.__init__(self, name=f'Client Handler {player_number}')
        self.settimeout(DEFAULT_TIMEOUT)
        self.bind((ip, port + player_number))
        self.setDaemon(True)
        self.player_number = player_number
        self.client_ip_address = client_ip_address
        self.server_manager = server_manager
        # send the player number when whe create the server client handler
        self._send_player_number()

    def _send_player_number(self):
        message = str(self.player_number).encode(FORMAT)
        self.sendto(message, self.client_ip_address)

    def receive_client_update(self):
        data, address_info = self.recvfrom(BUFFER_SIZE)
        if data:
            decoded_data = data.decode(FORMAT)
            print(decoded_data)
            return decoded_data

    def run(self):
        while True:
            response = self.receive_client_update()
            self.update_player_with_client_command(response)
            self.server_manager.debug()

    def update_player_with_client_command(self, response):
        self.server_manager.players[self.player_number - 1] = response

    def join(self, timeout=None):
        super().join(timeout=DEFAULT_TIMEOUT)
        self.close()
