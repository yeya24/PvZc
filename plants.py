import pygame

from animation import getImagesFromSpriteSheet
from config import *
from other import Sun
from sprite import Sprite


class Plant(Sprite):
    counter = 0
    # Изображение, которое будет отображаться при выборе этого растения
    shadow = None
    # Характеристики растения пишутуся здесь,
    # Чтобы был доступ до инициализации класса
    sunCost = 100
    health = 300
    recharge = 5
    reload = 0
    damage = 0

    def __init__(self, cell, anim_speed=None, images=None, image=None, size=None):
        if images is None and image is None:
            image = pygame.Surface(size)
        elif images is not None:
            self.images = images
            image = next(images)
        # Расположение в центре клетки
        super().__init__(cell.rect.x + (sizes["cell"][0] - size[0]) / 2,
                         cell.rect.y + (sizes["cell"][1] - size[1]) / 2,
                         image=image, size=size)
        # Частота обновления анимации
        self.animation_frame = anim_speed
        # Прочие характеристики
        self.coords = (cell.row, cell.col)

    def update(self, screen):
        if self.animation_frame is not None:
            self.counter += 1
            if self.counter % self.animation_frame == 0:
                self.image = next(self.images)

            self.counter %= self.animation_frame
        self._draw(screen)


class PeaShooter(Plant):
    shadow = pygame.image.load("assets/images/peaShooter_.png")

    sunCost = 100
    health = 300
    recharge = 5
    damage = 20
    reload = fps * 1.5

    def __init__(self, cell, projectiles):
        images, size = getImagesFromSpriteSheet("assets/images/peaShooter.png",
                                                13, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 30,
                         images=images, size=size)
        self.projectiles = projectiles

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.shot()

        self.counter %= self.reload * self.animation_frame
        self._draw(screen)

    def shot(self):
        # Создание зеленой пули
        b = PeashooterProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)


class Sunflower(Plant):
    shadow = pygame.image.load("assets/images/sunflower_.png")

    sunCost = 50
    health = 300
    recharge = 5
    reload = fps * 24

    def __init__(self, cell, suns_group):
        images, size = getImagesFromSpriteSheet("assets/images/sunflower.png",
                                                18, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 20,
                         images=images, size=size)
        self.suns_group = suns_group
        self.counter = fps * 17

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.generate_sun()

        self.counter %= self.reload * self.animation_frame
        self._draw(screen)

    def generate_sun(self):
        self.suns_group.add(
            Sun(self.rect.x, self.rect.top, self.rect.centery, True)
        )


class PotatoMine(Plant):
    shadow = pygame.image.load("assets/images/potatoMine_.png")

    sunCost = 25
    health = 300
    recharge = 20
    damage = 1800
    reload = fps * 2

    def __init__(self, cell):
        # TODO добавить взрыв при контакте с врагом
        self.images, _ = getImagesFromSpriteSheet("assets/images/potatoMineReady.png",
                                                  7, 4)
        self.arming, size = getImagesFromSpriteSheet("assets/images/potatoMineArming.png",
                                                     1, 3, size=sizes["plant"], cycle=False)
        self.explosion = pygame.transform.smoothscale(
            pygame.image.load("assets/images/potatoMineExplosion.png").convert_alpha(),
            sizes["potatoExp"])
        super().__init__(cell,
                         anim_speed=fps / 12,
                         image=self.arming[0],
                         size=size)
        self.armed = False
        self.detonation = 30

    def update(self, screen):
        if self.health > 0:
            self.counter += 1
            if not self.armed:
                if self.counter == self.reload:
                    self.image = next(self.images)
                    self.counter = 0
                    self.armed = True
                elif self.counter > self.reload * 2 / 3:
                    self.image = self.arming[2]
                elif self.counter > self.reload / 3:
                    self.image = self.arming[1]
            else:
                if self.counter == self.animation_frame:
                    self.image = next(self.images)
                    self.counter = 0
        else:
            self.detonation -= 1
            if not self.detonation:
                self.kill()
        self._draw(screen)

    def explode(self, enemy):
        self.image = self.explosion
        # Конфигурация положения изображения (т. к. размеры взрыва и обычные различаются)
        self.rect.x -= (sizes["potatoExp"][0] - sizes["cell"][0]) / 2
        self.rect.y -= (sizes["potatoExp"][1] - sizes["cell"][1]) / 1.2
        enemy.health -= self.damage
        enemy.check_alive()
        self.health = 0  # Для начала отображения изображения взрыва


class WallNut(Plant):
    shadow = pygame.transform.smoothscale(pygame.image.load("assets/images/wallNut_.png"),
                                          sizes["plant"])
    sunCost = 50
    health = 3600
    recharge = 20

    def __init__(self, cell):
        self.images, size = getImagesFromSpriteSheet("assets/images/wallNut.png",
                                                     1, 3, size=sizes["plant"], cycle=False)
        super().__init__(cell, image=self.images[0],
                         size=size)
        self.max_health = self.health

    def update(self, screen):
        # TODO добавить небольшое движение, использовать анимации
        if self.health < self.max_health * 2 / 3:
            self.image = self.images[1]
        elif self.health < self.max_health / 3:
            self.image = self.images[2]

        self._draw(screen)


class CherryBomb(Plant):
    sunCost = 150
    health = 200
    recharge = 35
    damage = 1800


class Repeater(Plant):
    sunCost = 200
    health = 300
    recharge = 5
    reload = fps * 1.5
    damage = 20


class SnowPea(Plant):
    shadow = pygame.image.load("assets/images/snowPea_.png")

    sunCost = 175
    health = 300
    recharge = 5
    reload = 1.5 * fps
    damage = 20

    def __init__(self, cell, projectiles):
        images, size = getImagesFromSpriteSheet("assets/images/snowPea.png",
                                                7, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 20,
                         images=images, size=size)
        self.projectiles = projectiles

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.shot()

        self.counter %= self.reload * self.animation_frame
        self._draw(screen)

    def shot(self):
        b = SnowProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)


class Chomper(Plant):
    sunCost = 150
    health = 300
    recharge = 5
    reload = fps * 42
    damage = 9999


class Projectile(Sprite):
    def __init__(self, x, y, row, speed, damage, image, size=None):
        super().__init__(x, y, image, size)
        self.speed = speed
        self.damage = damage
        self.row = row

    def deal_damage(self, target):
        target.health -= self.damage

    def update(self, screen):
        self.rect.x += self.speed
        self._draw(screen)
        if self.rect.x >= sizes["win"][0]:
            self.kill()


class PeashooterProjectile(Projectile):
    def __init__(self, x, y, row):
        super().__init__(x + 5, y + 5, row,
                         6, 20,
                         pygame.image.load("assets/images/peaShooterProjectile.png").
                         convert_alpha(),
                         size=sizes["projectile"])


class SnowProjectile(Projectile):
    freeze_time = fps * 1.5

    def __init__(self, x, y, row):
        super().__init__(x + 5, y + 5, row,
                         6, 20,
                         pygame.image.load("assets/images/snowPeaProjectile.png").
                         convert_alpha(),
                         size=sizes["projectile"])
