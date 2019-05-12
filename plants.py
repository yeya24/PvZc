import pygame

from config import *

from sprite import Sprite
from other import Sun

# Чтобы у локации был доступ к изображению выбранного растения
plant_images = {
    name: pygame.image.load(f"assets/images/{name.lower()}.png")
    for name in plants.keys()
}
map(pygame.Surface.convert_alpha, plant_images.values())


class Plant(Sprite):
    chars = {}
    counter = 0

    def __init__(self, cell, hp, image, size=None):
        # Расположение в центре клетки
        super().__init__(cell.rect.x + (sizes["cell"]["w"] - image.get_width()) / 2,
                         cell.rect.y + (sizes["cell"]["h"] - image.get_height()) / 2,
                         image, size)

        # Прочие характеристики
        self.hp = hp

    def take_damage(self, enemy):
        pass


class PeaShooter(Plant):
    chars = plants["PeaShooter"]

    def __init__(self, cell):
        # Словарь с характеристиками цветка
        super().__init__(cell, self.chars["toughness"],
                         plant_images["PeaShooter"])

        self.projectiles = pygame.sprite.Group()

        # Стреляет раз в полторы секнуды
        # Counter - счетчик обновления кадров
        self.shot_time = fps * 1.5

    def update(self, screen):
        self._draw(screen)

        self.counter += 1
        if self.counter == self.shot_time:
            self.shot()
            self.counter = 0

        if self.hp <= 0:
            self.kill()

        self.projectiles.update(screen)

    def shot(self):
        # Создание зеленой пули
        b = PeashooterProjectile(*self.rect.midtop)
        self.projectiles.add(b)


class Sunflower(Plant):
    chars = plants["Sunflower"]

    def __init__(self, cell, suns_grop):
        super().__init__(cell, self.chars["toughness"],
                         plant_images["Sunflower"])
        self.suns_group = suns_grop
        self.shot_time = fps * 24
        self.counter = fps * 17

    def update(self, screen):
        self._draw(screen)

        self.counter += 1
        if self.counter == self.shot_time:
            self.generate_sun()
            self.counter = 0

        if self.hp <= 0:
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

    def __init__(self, x, y, speed, damage, image, size=None):
        super().__init__(x, y, image, size)
        self.speed = speed
        self.damage = damage

    def deal_damage(self):
        ...

    def update(self, screen):
        self.rect.x += self.speed
        self._draw(screen)
        if self.rect.x >= sizes["win"]["w"]:
            self.kill()


class PeashooterProjectile(Projectile):
    """Класс обычной зеленой пули"""

    def __init__(self, x, y):
        super().__init__(x + 5, y + 5, 6, 20,
                         pygame.image.load("assets/images/peashooterprojectile.png").
                         convert_alpha(),
                         size=tuple(sizes["projectile"].values()))


class SnowProjectile(Projectile):
    pass
