import pygame

from misc import get_images_from_sprite_sheet
from ._plant import _Plant


class WallNut(_Plant):
    """
    Wall-Nut simply can absorb a lot of damage
    """
    shadow = pygame.image.load("assets/plants/wallNut_.png")
    sunCost = 50
    health = 3600
    recharge = 20

    def __init__(self, cell):
        self.images, size = get_images_from_sprite_sheet("assets/plants/wallNut.png",
                                                         1, 3, cycle=False)
        super().__init__(cell, image=self.images[0])
        self.max_health = self.health

    def update(self, screen):
        # TODO add motion
        if self.health < self.max_health * 2 / 3:
            self.image = self.images[1]
        elif self.health < self.max_health / 3:
            self.image = self.images[2]

        self._draw(screen)
