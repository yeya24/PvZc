import pygame

import config as c
from sprites import Sprite


class Tile(Sprite):
    """
    Class for cell that has plants planted on
    """

    def __init__(self, col: int, row: int, can_build: bool):
        super().__init__(col * c.sizes["cell"][0] + c.pads["game"][0],
                         row * c.sizes["cell"][1] + c.pads["game"][1],
                         size=c.sizes["cell"])
        self.row = row
        self.col = col
        self.coords = (row, col)
        self.can_build = can_build
        self.planted = pygame.sprite.GroupSingle()
        self.plant_sound = pygame.mixer.Sound("assets/audio/plant.wav")
        self.shovel_sound = pygame.mixer.Sound("assets/audio/Shovel.ogg")

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
            elif plant.__name__ in c.passive_plants:
                self.planted.add(plant(self))
            else:
                self.planted.add(plant(self, projectiles))
            self.plant_sound.play()
            return True
        return False

    def remove_plant(self) -> bool:
        """
        Player removes player from the cell using shovel
        :return: True if plant has been removed
        """
        for s in self.planted:
            s.kill()
            self.shovel_sound.play()
            return True
        return False

    def get_middle_pos(self, image):
        """
        Return tuple containing x and y positions
        for displaying plant image in the middle of the cell
        :param image: Surface
        :return: (x, y)
        """
        return (self.rect.x + (self.rect.width - image.get_width()) / 2,
                self.rect.y + (self.rect.height - image.get_height()) / 2)

    def isempty(self) -> bool:
        """
        Checks if tile contains no plant
        :return: bool
        """
        return not len(self.planted)
