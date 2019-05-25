import pygame

from config import pads, sizes
from sprites import Sprite


class Tile(Sprite):
    """
    Class for cell that has plants planted on it
    """

    def __init__(self, col: int, row: int, can_build: bool):
        #  TODO добавить тени под растения
        super().__init__(col * sizes["cell"][0] + pads["game"][0],
                         row * sizes["cell"][1] + pads["game"][1],
                         size=sizes["cell"])
        self.row = row
        self.col = col
        self.coords = (row, col)
        self.can_build = can_build
        self.planted = pygame.sprite.GroupSingle()
        self.plant_sound = pygame.mixer.Sound("assets/audio/plant.wav")

    def update(self, screen):
        if self.planted:
            self.planted.update(screen)

    def plant(self, plant: type, suns: pygame.sprite.Group,
              projectiles: pygame.sprite.Group) -> bool:
        """
        Plants plant on the cell and gives arguments depending on the type
        :param plant: plant to be planted type
        :param suns: sun group from location for sunflower
        :param projectiles: projectile group for peashooters
        :return: True if planted
        """
        if self.can_build and self.isempty():
            if plant.__name__ == "Sunflower":
                self.planted.add(plant(self, suns))
            elif plant.__name__ in ["WallNut", "PotatoMine",
                                    "Chomper", "CherryBomb",
                                    "Jalapeno", "Squash"]:
                self.planted.add(plant(self))
            else:
                self.planted.add(plant(self, projectiles))
            self.plant_sound.play()
            return True
        return False

    def isempty(self) -> bool:
        """
        Checks if tile contains no plant
        :return: bool
        """
        return not len(self.planted)
