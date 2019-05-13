from config import *

from sprite import Sprite


class Tile(Sprite):
    def __init__(self, col, row, can_build):
        super().__init__(x=col * sizes["cell"][0] + pads["game"][0],
                         y=row * sizes["cell"][1] + pads["game"][1],
                         size=sizes["cell"])
        # Позиция в матрице
        self.row = row
        self.col = col
        # можно строить?
        self.can_build = can_build

        # Игровые характеристики
        # Что находится сверху (горшок, цветок)
        self.on_top = None

    def update(self, screen):
        if self.on_top:
            self.on_top.update(screen)

    def plant(self, plant, suns, projectiles):
        if self.can_build and self.on_top is None:
            # Подсолнухам нужен доступ к группе солнц
            if plant.__name__ == "Sunflower":
                self.on_top = plant(self, suns)
            # Орех никак не взаимодействует с зомби и солнцами
            elif plant.__name__ == "WallNut":
                self.on_top = plant(self)
            # Стреляющим растениям нужен доступ к групппе пуль
            else:
                self.on_top = plant(self, projectiles)
            return True
        return False


class Grass(Tile):
    def __init__(self, col, row):
        super().__init__(col, row, True)
