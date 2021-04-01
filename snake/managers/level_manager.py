import json
import os


class LevelManager:

    def __init__(self):
        with open(os.path.join("./snake/assets/levels/levels.json"), 'r+') as file:
            self.levels = json.load(file)

    def get_level(self, level):
        if level >= len(self.levels):
            return
        return self.levels[level]
