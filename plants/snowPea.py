import pygame

from config import fps, sizes
from misc import get_images_from_sprite_sheet, lcm
from projectiles import SnowProjectile
from .plant import Plant


class SnowPea(Plant):
    """
    Snow pea is a peashooter which shoots freezing projectiles
    """
    shadow = pygame.image.load("assets/plants/snowPea_.png")

    sunCost = 175
    health = 300
    recharge = 5
    reload = 1.5 * fps
    damage = 20

    def __init__(self, cell, projectiles):
        images, size = get_images_from_sprite_sheet("assets/plants/snowPea.png",
                                                    7, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 20,
                         images=images, size=size)
        self.projectiles = projectiles
        self.shot_sound = pygame.mixer.Sound("assets/audio/throw.wav")

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.shot()

        self.counter %= lcm(self.reload, self.animation_frame)
        self._draw(screen)

    def shot(self):
        """
        Creates SnowProjectile object
        and adds it to the location projectiles group
        :return: None
        """
        b = SnowProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)
        self.shot_sound.play()
