import pygame

from config import *

from sprite import Sprite
from other import Sun
from animation import getImagesFromSpriteSheet

# Чтобы у локации был доступ к изображению выбранного растения
plant_images = {
    name: pygame.image.load(f"assets/images/{name.lower()}.png")
    for name in plants.keys()
}
map(pygame.Surface.convert_alpha, plant_images.values())


class Plant(Sprite):
    chars = {}
    counter = 0

    def __init__(self, cell, health, anim_speed, images, size):
        # Расположение в центре клетки
        super().__init__(cell.rect.x + (sizes["cell"][0] - size[0]) / 2,
                         cell.rect.y + (sizes["cell"][1] - size[1]) / 2,
                         image=next(images), size=size)
        self.images = images
        # Анимация
        self.animation_frame = anim_speed

        # Прочие характеристики
        self.cell = cell
        self.health = health

    def update(self, screen):

        self.counter += 1
        if self.counter == self.animation_frame:
            self.image = next(self.images)
            self.counter = 0

        if self.health <= 0:
            self.kill()

        self._draw(screen)

    def take_damage(self, enemy):
        pass


class PeaShooter(Plant):
    chars = plants["PeaShooter"]

    def __init__(self, cell, projectiles):
        # Словарь с характеристиками цветка
        super().__init__(cell, self.chars["toughness"], fps // 30,
                         * getImagesFromSpriteSheet("assets/images/peashooter.png",
                                                    13, 3, size=sizes["plant"]))

        self.projectiles = projectiles

        # Стреляет раз в полторы секнуды
        # Counter - счетчик обновления кадров
        self.shot_time = self.chars["reload"]

    def update(self, screen):

        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)

        if self.counter % self.shot_time == 0:
            self.shot()

        self.counter %= self.shot_time * self.animation_frame
        self._draw(screen)

        if self.health <= 0:
            self.kill()

    def shot(self):
        # Создание зеленой пули
        b = PeashooterProjectile(*self.rect.midtop, self.cell.row)
        self.projectiles.add(b)


class Sunflower(Plant):
    chars = plants["Sunflower"]

    def __init__(self, cell, suns_group):
        super().__init__(cell, self.chars["toughness"], fps // 20,
                         *getImagesFromSpriteSheet("assets/images/sunflower.png",
                                                   18, 3, size=sizes["plant"]))
        self.suns_group = suns_group
        self.shot_time = self.chars["reload"]
        self.counter = fps * 17

    def update(self, screen):

        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)

        if self.counter % self.shot_time == 0:
            self.generate_sun()

        self.counter %= self.shot_time * self.animation_frame
        self._draw(screen)

        if self.health <= 0:
            self.kill()

    def generate_sun(self):
        self.suns_group.add(
            Sun(self.rect.x, self.rect.top, self.rect.centery, True)
        )


class PotatoMine(Plant):
    pass


class WallNut(Plant):
    pass


class CherryBomb(Plant):
    pass


class Repeater(Plant):
    pass


class SnowPea(Plant):
    pass


class Chomper(Plant):
    pass


class Projectile(Sprite):
    """Базовый класс для пуль"""

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
    """Класс обычной зеленой пули"""

    def __init__(self, x, y, row):
        super().__init__(x + 5, y + 5, row,
                         6, 20,
                         pygame.image.load("assets/images/peashooterprojectile.png").
                         convert_alpha(),
                         size=sizes["projectile"])


class SnowProjectile(Projectile):
    pass
