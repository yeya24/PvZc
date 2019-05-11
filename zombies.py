import pygame
from pygame.locals import *

from config import *
from sprite import Sprite


class Zombie(Sprite):

    def __init__(self, *args):
        super().__init__(*args)
        ...

    def move(self):
        ...

    def take_damage(self, bullet):
        ...

    def deal_damage(self, enemy):
        ...


class NormalZombie(Zombie):
    pass


class FlagZombie(Zombie):
    pass


class ConeHeadZombie(Zombie):
    pass


class PoleVaultingZombie(Zombie):
    pass


class BucketHeadZombie(Zombie):
    pass
