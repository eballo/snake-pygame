
class ServerManager:

    def __init__(self):
        self.clients = []
        self.players = [
            {"direction": "UP", "positions": [[120, 280], [140, 280], [160, 280]], "color": [0, 255, 0], "length": 3,
             "lives": 1}
            ,
            {"direction": "DOWN", "positions": [[400, 340], [400, 320], [400, 300]], "color": [255, 0, 0], "length": 3,
             "lives": 1}
        ]

    def debug(self):
        print("----")
        print(f"Total of players: {len(self.players)}")
        for player in self.players:
            print(player)
