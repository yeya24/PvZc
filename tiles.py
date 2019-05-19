import pygame

from config import *

from sprite import Sprite


class Tile(Sprite):
    def __init__(self, col, row, can_build):
        #  TODO добавить тени под растения
        super().__init__(col * sizes["cell"][0] + pads["game"][0],
                         row * sizes["cell"][1] + pads["game"][1],
                         size=sizes["cell"])
        # Позиция в матрице
        self.row = row
        self.col = col
        self.coords = (row, col)
        # можно строить
        self.can_build = can_build
        # Игровые характеристики
        # Что находится сверху (горшок, цветок)
        self.planted = pygame.sprite.GroupSingle()

    def update(self, screen):
        if self.planted:
            self.planted.update(screen)

    def plant(self, plant, suns, projectiles):
        if self.can_build and self.isempty():
            # Подсолнухам нужен доступ к группе солнц
            if plant.__name__ == "Sunflower":
                self.planted.add(plant(self, suns))
            # Орех никак не взаимодействует с зомби и солнцами
            elif plant.__name__ in ["WallNut", "PotatoMine"]:
                self.planted.add(plant(self))
            # Стреляющим растениям нужен доступ к групппе пуль
            else:
                self.planted.add(plant(self, projectiles))
            return True
        return False

    def isempty(self):
        return not len(self.planted)


class Grass(Tile):
    def __init__(self, col, row):
        super().__init__(col, row, True)