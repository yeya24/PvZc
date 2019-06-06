import pygame

import config as c
from .sprite import Sprite


class Shovel(Sprite):
    """
    Duck typing class for shovel object used to remove plants
    """

    def __init__(self, x: int, y: int):
        super().__init__(x + 10, y + 10,
                         image=pygame.image.load("assets/misc/shovel.png").convert_alpha(),
                         size=c.sizes["cell"])
        self.starting_pos = (x, y)
        self.taken = False

    def take(self):
        """
        Says top menu not to draw it
        :return: self
        """
        self.taken = True
        return self

    def put_back(self):
        """
        Says top menu to draw and use
        :return: None
        """
        self.taken = False

    def can_take(self, mouse_pos: tuple) -> bool:
        """
        Checks if player clicked on the shovel
        :param mouse_pos: (x, y)
        :return: bool
        """
        return self.rect.collidepoint(mouse_pos)

    def get_shadow(self):
        """
        Same method as in the plant class
        :return: Surface
        """
        return self.image
