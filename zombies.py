import pygame
from pygame.locals import *

from config import *
from sprite import Sprite

from animation import getImagesFromSpriteSheet, get_transparent_image


# Игра открывает txt файл с конфигурацией уровня
# Там указан порядок появления зомби
# Случайно выбирается линия поялвения


class Zombie(Sprite):

    def __init__(self, row, health, speed, images, size):
        super().__init__(
            sizes["win"][0],
            pads["game"][1] + (row - 3 / 4) * sizes["cell"][1],
            size=size
        )
        # Анимация
        self.images = images
        # Частота смены кадров анимации
        self.animation_frame = fps / 10
        self.counter = 0
        # Поскольку скорость меньше чем 1, то нужно использовать окургление
        self.x = self.rect.x
        # Характеристики
        self.health = health
        self.speed = speed
        # Позиция на поле
        self.cell = XCells + 1
        self.row = row

    def update(self, screen):
        self._draw(screen)

        self.counter += 1
        if self.counter == self.animation_frame:
            self.image = next(self.images)
            self.counter = 0

        # Движение
        self.x -= self.speed
        self.rect.x = int(self.x) + 1

    def take_damage(self, bullet):
        self.health -= bullet.damage
        if self.health <= 0:
            self.kill()
        bullet.kill()

        self.image = get_transparent_image(self.image,
                                           density=64, alpha=5, special_flag=BLEND_RGBA_ADD)

    def deal_damage(self, enemy):
        ...


class NormalZombie(Zombie):
    chars = zombies["NormalZombie"]

    def __init__(self, row):
        super().__init__(
            row, self.chars["hp"], self.chars["speed"],
            *getImagesFromSpriteSheet("assets/images/normalzombie.png",
                                      10, 5, ratio=4 / 5)
        )


class FlagZombie(Zombie):
    pass


class ConeHeadZombie(Zombie):
    chars = zombies["ConeHeadZombie"]

    def __init__(self, row):
        super().__init__(
            row, self.chars["hp"], self.chars["speed"],
            *getImagesFromSpriteSheet("assets/images/coneheadzombie.png",
                                      10, 5, ratio=4 / 5)
        )


class PoleVaultingZombie(Zombie):
    pass


class BucketHeadZombie(Zombie):
    chars = zombies["BucketHeadZombie"]

    def __init__(self, row):
        super().__init__(
            row, self.chars["hp"], self.chars["speed"],
            *getImagesFromSpriteSheet("assets/images/bucketheadzombie.png",
                                      10, 5, ratio=4 / 5)
        )
