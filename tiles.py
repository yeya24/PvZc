import pygame

from config import sizes, pads
from sprite import Sprite


class Tile(Sprite):
    def __init__(self, col: int, row: int, can_build: bool):
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
        self.plant_sound = pygame.mixer.Sound("audio/plant.wav")

    def update(self, screen):
        if self.planted:
            self.planted.update(screen)

    def plant(self, plant: type, suns: "pygame.sprite.Group",
              projectiles: "pygame.sprite.Group") -> bool:
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
            self.plant_sound.play()
            return True
        return False

    def isempty(self) -> bool:
        return not len(self.planted)


class Grass(Tile):
    def __init__(self, col, row):
        super().__init__(col, row, True)
