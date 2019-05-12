import pygame
from pygame.locals import *

from config import *
from sprite import Sprite

from math import ceil


# Игра открывает txt файл с конфигурацией уровня
# Там указан порядок появления зомби
# Случайно выбирается линия поялвения


class Zombie(Sprite):

    def __init__(self, row, health, speed, image=None, size=None):
        super().__init__(
            sizes["win"]["w"],
            pads["game"]["y"] + (row + 1 / 2) * sizes["cell"]["h"],
            image=image, size=size
        )
        self.x = self.rect.x
        # Характеристики
        self.health = health
        self.speed = speed
        self.cell = XCells + 1

    def update(self, screen):
        # Движение
        self.x -= self.speed
        self.rect.x = ceil(self.x)
        self._draw(screen)

    def take_damage(self, bullet):
        ...

    def deal_damage(self, enemy):
        ...


class NormalZombie(Zombie):
    chars = zombies["NormalZombie"]

    def __init__(self, row):
        super().__init__(
            row, self.chars["hp"], self.chars["speed"],
            image=pygame.image.load("assets/images/empty.png").convert_alpha()
        )


class FlagZombie(Zombie):
    pass


class ConeHeadZombie(Zombie):
    pass


class PoleVaultingZombie(Zombie):
    pass


class BucketHeadZombie(Zombie):
    pass
