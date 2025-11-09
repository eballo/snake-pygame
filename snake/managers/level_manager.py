import json
import os


class LevelManager:

    def __init__(self) -> None:
        with open(os.path.join("./snake/assets/levels/levels.json"), "r+") as file:
            self.levels = json.load(file)

    def get_level(self, level: int) -> dict | None:
        if level >= len(self.levels):
            return None
        return self.levels[level]
