import pygame

from animation import get_images_from_sprite_sheet
from config import fps, sizes
from other import Sun, lcm
from projectiles import PeashooterProjectile, SnowProjectile
from sprite import Sprite


class Plant(Sprite):
    """
    Base plant class
    """
    counter = 0
    # Image which is displayed when plant is chosen to plant
    shadow = None
    # Characteristics
    sunCost = 100
    health = 300
    recharge = 5
    reload = 0
    damage = 0

    def __init__(self, cell, anim_speed: int = None,
                 images: list = None, image: pygame.Surface = None,
                 size: tuple = None):
        if images is None and image is None:
            image = pygame.Surface(size)
        elif images is not None:
            self.images = images
            image = next(images)
        # Positioning in the middle of the cell
        super().__init__(cell.rect.x + (sizes["cell"][0] - size[0]) / 2,
                         cell.rect.y + (sizes["cell"][1] - size[1]) / 2,
                         image=image, size=size)
        # Animations speed
        self.animation_frame = anim_speed

        self.coords = cell.coords
        # Sound of being eaten by zombie
        self.death_sound = pygame.mixer.Sound("audio/gulp.wav")

    def check_alive(self):
        """
        Kills itself if health if below of equals zero
        :return: None
        """
        if self.health <= 0:
            self.kill()
            self.death_sound.play()

    def update(self, screen):
        """
        Makes plant act and draws it
        :param screen: pygame.display
        :return: None
        """
        pass


class PeaShooter(Plant):
    """
    The most basic plant which shoots peas
    """
    shadow = pygame.image.load("plants/peaShooter_.png")

    sunCost = 100
    health = 300
    recharge = 5
    damage = 20
    reload = fps * 1.5

    def __init__(self, cell, projectiles: pygame.sprite.Group):
        images, size = get_images_from_sprite_sheet("plants/peaShooter.png",
                                                    13, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 30,
                         images=images, size=size)
        self.projectiles = projectiles

        self.shot_sound = pygame.mixer.Sound("audio/throw.wav")

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.shot()

        self.counter %= lcm(self.reload * self.animation_frame)
        self._draw(screen)

    def shot(self):
        b = PeashooterProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)
        self.shot_sound.play()


class Sunflower(Plant):
    """
    Sunflower plant drops suns
    """
    shadow = pygame.image.load("plants/sunflower_.png")

    sunCost = 50
    health = 300
    recharge = 5
    reload = fps * 24

    def __init__(self, cell, suns_group):
        images, size = get_images_from_sprite_sheet("plants/sunflower.png",
                                                    18, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 20,
                         images=images, size=size)
        self.suns_group = suns_group
        self.counter = fps * 17

        self.sun_sound = pygame.mixer.Sound("audio/throw.wav")

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.generate_sun()

        self.counter %= lcm(self.reload, self.animation_frame)
        self._draw(screen)

    def generate_sun(self):
        """
        Adds sun to the location suns group
        :return: None
        """
        self.suns_group.add(
            Sun(self.rect.x, self.rect.top, self.rect.centery, True)
        )
        self.sun_sound.play()


class PotatoMine(Plant):
    """
    Potato mine explodes with giant damage
     after being armed for several seconds
    """
    shadow = pygame.image.load("plants/potatoMine_.png")

    sunCost = 25
    health = 300
    recharge = 20
    damage = 1800
    reload = fps * 14

    def __init__(self, cell):
        self.images, _ = get_images_from_sprite_sheet("plants/potatoMineReady.png",
                                                      7, 4)
        self.arming, size = get_images_from_sprite_sheet("plants/potatoMineArming.png",
                                                         1, 3, size=sizes["plant"], cycle=False)
        self.explosion = pygame.transform.smoothscale(
            pygame.image.load("plants/potatoMineExplosion.png").convert_alpha(),
            sizes["potatoExp"])
        super().__init__(cell,
                         anim_speed=fps // 12,
                         image=self.arming[0],
                         size=size)
        self.armed = False
        self.detonation = 60
        self.detonation_sound = pygame.mixer.Sound("audio/potato_mine.wav")

    def update(self, screen):
        if self.health > 0:
            self.counter += 1
            if not self.armed:
                if self.counter == self.reload:
                    self.image = next(self.images)
                    self.counter, self.armed = 0, True
                elif self.counter > self.reload * 2 // 3:
                    self.image = self.arming[2]
                elif self.counter > self.reload // 3:
                    self.image = self.arming[1]
            elif self.counter == self.animation_frame:
                self.image = next(self.images)
                self.counter = 0
        else:
            self.detonation -= 1
            if not self.detonation:
                self.kill()
        self._draw(screen)

    def explode(self, enemy):
        """
        Deals damage to zombie
         and displays explosion image
        :param enemy: Zombie
        :return: None
        """
        self.image = self.explosion
        # Конфигурация положения изображения (т. к. размеры взрыва и обычные различаются)
        self.rect.x -= (sizes["potatoExp"][0] - sizes["cell"][0]) // 2
        self.rect.y -= (sizes["potatoExp"][1] - sizes["cell"][1]) // 1.2
        enemy.health -= self.damage
        enemy.check_alive()
        self.health = 0  # Для начала отображения изображения взрыва
        self.detonation_sound.play()


class WallNut(Plant):
    """
    Wall nut simply can absorb a lot of damage
    """
    shadow = pygame.transform.smoothscale(pygame.image.load("plants/wallNut_.png"),
                                          sizes["plant"])
    sunCost = 50
    health = 3600
    recharge = 20

    def __init__(self, cell):
        self.images, size = get_images_from_sprite_sheet("plants/wallNut.png",
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
    """
    Cherry bomb explodes in the 3 cell diameter
    """
    shadow = None

    sunCost = 150
    health = 200
    recharge = 35
    damage = 1800


class Repeater(Plant):
    """
    Repeater is better peashooter which shoots two peas in a row
    """
    shadow = pygame.image.load("plants/repeater_.png")

    sunCost = 200
    health = 300
    recharge = 5
    reload = fps * 1.5
    damage = 20

    def __init__(self, cell, projectiles):
        images, size = get_images_from_sprite_sheet("plants/repeater.png",
                                                    14, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 20,
                         images=images, size=size)
        self.projectiles = projectiles
        self.shot_sound = pygame.mixer.Sound("audio/throw.wav")

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.shot()
        elif (self.counter - 10) % self.reload == 0:
            self.shot()

        self.counter %= lcm(self.reload, self.reload + 10, self.animation_frame)
        self._draw(screen)

    def shot(self):
        b = PeashooterProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)
        self.shot_sound.play()


class SnowPea(Plant):
    """
    Snow pea is a peashooter which shoots freezing projectiles
    """
    shadow = pygame.image.load("plants/snowPea_.png")

    sunCost = 175
    health = 300
    recharge = 5
    reload = 1.5 * fps
    damage = 20

    def __init__(self, cell, projectiles):
        images, size = get_images_from_sprite_sheet("plants/snowPea.png",
                                                    7, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 20,
                         images=images, size=size)
        self.projectiles = projectiles
        self.shot_sound = pygame.mixer.Sound("audio/throw.wav")

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.shot()

        self.counter %= lcm(self.reload, self.animation_frame)
        self._draw(screen)

    def shot(self):
        b = SnowProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)
        self.shot_sound.play()


class Chomper(Plant):
    shadow = None

    sunCost = 150
    health = 300
    recharge = 5
    reload = fps * 42
    damage = -1


class Squash(Plant):
    shadow = None

    sunCost = 50
    recharge = 20
    damage = 1800


class Jalapeno(Plant):
    pass
