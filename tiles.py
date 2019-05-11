import pygame
from pygame.locals import *

from config import *

from sprite import Sprite


class Tile(Sprite):
    def __init__(self, col, row, can_build):
        # TODO настроить положение с учетом рамки
        super().__init__(x=col * sizes["cell"]["w"] + pads["game"]["x"],
                         y=row * sizes["cell"]["h"] + pads["game"]["y"],
                         size=(sizes["cell"]["w"], sizes["cell"]["h"]))
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

    def plant(self, plant, suns):
        if self.can_build and self.on_top is None:
            # Подсолныхам нужен доступ к группе солнц
            if plant.__name__ == "Sunflower":
                self.on_top = plant(self, suns)
            else:
                self.on_top = plant(self)
            return True
        return False


class Grass(Tile):
    def __init__(self, col, row):
        super().__init__(col, row, True)
