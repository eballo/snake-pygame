import socket
import threading

from snake.settings import PORT, ADDRESS, HEADER, FORMAT, DISCONNECT_MESSAGE, SERVER


class Server():
    SERVER = socket.gethostbyname("localhost")
    ADDRESS = (SERVER, PORT)

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDRESS)

    def handle_client(self, connection, address):
        print(f'[NEW CONNECTION] {address} connected')

        connected = True
        while connected:
            msg_length = connection.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg = connection.recv(int(msg_length)).decode(FORMAT)

                if msg == DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{address}] {msg}")

    def start(self):
        self.server.listen()
        print(f"[LISTENING] server is listening on {SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f'[ACTIVE CONNECTION] {threading.active_count() - 1 }')


if __name__ == '__main__':
    print("[STARTING] server is starting ...")
    server = Server()
    server.start()
