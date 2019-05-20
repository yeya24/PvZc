import pygame
from pygame.locals import *

from animation import getImagesFromSpriteSheet, transform_image
from config import *
from sprite import Sprite


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
        # Текущее растение для атаки
        self.eating = pygame.sprite.GroupSingle()
        # Заморозка идет на какое-то число секунд, в это время скорости снижаются
        self.frozen = False
        self.frozen_reload = self.reload * 2
        self.frozen_speed = self.speed / 2
        # После попадания пули в зомби он на некоторое число секунд становится белее
        self.shot = False
        # Позиция на поле
        self.col = XCells + 1
        self.row = row

    def update(self, screen):
        self.counter += 1
        # Обновление анимации ходьбы
        # Или нанесение урона и анимация поедания
        # TODO анимация поедания
        if not self.busy():  # Если зомби не ест
            if self.counter % self.animation_frame == 0:
                self.image = next(self.images)
                if self.frozen:
                    self.image = transform_image(self.image, r=0, g=0, b=128, alpha=5,
                                                 special_flag=BLEND_RGBA_ADD)
                if self.shot:
                    self.shot = False
                    self.image = transform_image(self.image,
                                         r=64, g=64, b=64, alpha=5, special_flag=BLEND_RGBA_ADD)
            # Движение
            if not self.frozen:
                self.x -= self.speed
            else:
                self.frozen -= 1
                self.x -= self.frozen_speed
            self.rect.x = int(self.x) + 1
        else:
            # Нанесение урона раз в какой-то промежуток времени
            if not self.frozen:
                if self.counter % self.reload == 0:
                    self.deal_damage()
            else:
                self.frozen -= 1
                if self.counter % self.frozen_reload == 0:
                    self.deal_damage()

        self.counter %= self.reload * self.animation_frame
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

    def check_alive(self):
        if self.health <= 0:
            self.kill()

    def take_damage(self, bullet):
        self.health -= bullet.damage
        self.check_alive()
        bullet.kill()

        if bullet.__class__.__name__ == "SnowProjectile":
            self.frozen = bullet.freeze_time
            # "Замораживает" зомби - делает изображение синим начиная с текущего
            self.image = transform_image(self.image, r=0, g=0, b=128, alpha=5,
                                         special_flag=BLEND_RGBA_ADD)

        self.shot = True

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
