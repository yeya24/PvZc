import pygame
from pygame.locals import *

from config import *
from sprite import Sprite

from animation import getImagesFromSpriteSheet, transform_image


# Игра открывает txt файл с конфигурацией уровня
# Там указан порядок появления зомби
# Случайно выбирается линия поялвения


class Zombie(Sprite):
    # Частота смены анимации
    animation_frame = fps / 10
    counter = 0
    # Характеристики (по стандарту обычного зомби)
    health = 200
    speed = 1 / 5
    damage = 100
    reload = fps

    def __init__(self, row, images, size):
        super().__init__(
            sizes["win"][0],
            pads["game"][1] + (row - 3 / 4) * sizes["cell"][1],
            image=next(images), size=size
        )
        # Анимация
        # Итератор бесконечного цикла, меняющего изображения
        self.images = images
        # Поскольку скорость меньше чем 1, то нужно использовать окургление
        self.x = self.rect.x
        # Характеристики
        self.eating = pygame.sprite.GroupSingle()
        # Позиция на поле
        self.col = XCells + 1
        self.row = row

    def update(self, screen):
        self.counter += 1
        # Обновление анимации ходьбы
        # Или нанесение урона и анимация поедания
        # TODO анимация поедания
        if not self.busy():
            if self.counter % self.animation_frame == 0:
                self.image = next(self.images)
            # Движение если зомби не ест
            self.x -= self.speed
            self.rect.x = int(self.x) + 1
        else:
            # Нанесение урона раз в какой-то промежуток времени
            if self.counter % self.reload == 0:
                self.deal_damage()

        self.counter %= self.reload
        # Обновление координаты клетки игрового поля
        self.col = (self.rect.x - pads["game"][0] + sizes["cell"][0] / 2) // sizes["cell"][0]
        self._draw(screen)

    def busy(self):
        # Проверка, есть ли зомби
        return len(self.eating)

    def coords(self):
        # Координаты на игровом поле
        return self.row, self.col

    def change_target(self, enemy):
        # Смена цели
        self.eating.add(enemy)

    def take_damage(self, bullet):
        self.health -= bullet.damage
        if self.health <= 0:
            self.kill()
        bullet.kill()
        # Небольшое остветление изображения
        # TODO сделать с следующего кадра
        self.image = transform_image(self.image,
                                     density=64, alpha=5, special_flag=BLEND_RGBA_ADD)

    def deal_damage(self):
        self.eating.sprite.health -= self.damage
        if self.eating.sprite.health <= 0:
            self.eating.sprite.kill()


class NormalZombie(Zombie):

    def __init__(self, row):
        images, size = getImagesFromSpriteSheet("assets/images/normalZombie.png",
                                                10, 5, ratio=4 / 5)

        super().__init__(row, images, size)


class FlagZombie(Zombie):

    def __init__(self, row):
        images, size = getImagesFromSpriteSheet("assets/images/flagZombie.png",
                                                10, 5, ratio=4 / 5)

        super().__init__(row, images, size)


class ConeHeadZombie(Zombie):
    health = 560

    def __init__(self, row):
        images, size = getImagesFromSpriteSheet("assets/images/coneHeadZombie.png",
                                                10, 5, ratio=4 / 5)
        super().__init__(row, images, size)


class PoleVaultingZombie(Zombie):
    health = 340


class BucketHeadZombie(Zombie):
    health = 1300

    def __init__(self, row):
        images, size = getImagesFromSpriteSheet("assets/images/bucketHeadZombie.png",
                                                10, 5, ratio=4 / 5)
        super().__init__(row, images, size)
