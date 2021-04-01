from snakeserver.server import SnakeServer

if __name__ == '__main__':
    print("[STARTING] Snake Server is starting ...")
    server = SnakeServer()
    server.start()