
class ServerManager:

    def __init__(self):
        self.clients = []
        self.players = [0, 0]

    def debug(self):
        print("----")
        print(f"Total of players: {len(self.players)}")
        for player in self.players:
            print(player)
