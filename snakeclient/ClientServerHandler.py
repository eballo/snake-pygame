import random
import threading
import socket
from time import sleep

from snakeserver.settings import DEFAULT_TIMEOUT, COMMAND_CLIENT_CONNECT, FORMAT, BUFFER_SIZE


class ClientServerHandler(socket.socket, threading.Thread):

    def __init__(self, bind_address, server_address):
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)
        threading.Thread.__init__(self)
        self.settimeout(DEFAULT_TIMEOUT)
        self.setDaemon(True)
        self.bind(bind_address)
        self.server_address = server_address
        self.player_number = -1

    def run(self):
        self.connect()
        self.player_number = self.receive_player_number()
        print(f"player number: {self.player_number}")

        while True:
            #     game_update_json = self.receive_game_update_json()
            #     self.pong_world.update_with_json(game_update_json)
            text = random.randint(1, 1000)
            sleep(2)
            self.send_client_update(str(text))

    def __del__(self):
        self.close()

    def connect(self):
        message = COMMAND_CLIENT_CONNECT.encode(FORMAT)
        print(f'message:{message}, address: {self.server_address}')
        self.sendto(message, self.server_address)
        return

    def receive_player_number(self):
        data, address = self.recvfrom(BUFFER_SIZE)
        if data is None:
            return -1
        decoded = data.decode(FORMAT)
        try:
            player_number = int(decoded)
            print('player_number', player_number)
        except ValueError as err:
            raise ValueError(err + ' Should have received an integer!')

        # OVERWRITE self.server_address to the one received, since that will be address of the client handler
        self.server_address = address
        return player_number

    # def receive_game_update_json(self, return_dict=None):
    #     data, address = self.recvfrom(self.BUFFER_SIZE)
    #     if data is None:
    #         raise ValueError('Unable to receive game update!')
    #         return -1
    #     decoded_json = data.decode('utf-8')
    #     try:
    #         # pong_update = json.loads(decoded_json, object_hook=pong.common.from_json)
    #         pass
    #     except json.JSONDecodeError as err:
    #         raise json.JSONDecodeError(err + ' Not a JSON string!')
    #     if return_dict is not None and isinstance(return_dict, dict):
    #         return_dict['game_update_json'] = decoded_json
    #     return decoded_json

    def send_client_update(self, text):
        message = text.encode(FORMAT)
        print(f'message:{message}, address: {self.server_address}')
        self.sendto(message, self.server_address)
