import socket

from snakeserver.settings import DEFAULT_IP_SERVER, DEFAULT_PORT, FORMAT, BUFFER_SIZE


class Client():

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((DEFAULT_IP_SERVER, DEFAULT_PORT))

    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (BUFFER_SIZE - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
