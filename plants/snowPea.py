import pygame

import config as c
from misc import get_images_from_sprite_sheet
from projectiles import SnowProjectile
from ._plant import _Plant


class SnowPea(_Plant):
    """
    Snow pea is a peashooter which shoots freezing projectiles
    """
    shadow = pygame.image.load("assets/plants/snowPea_.png")

    sunCost = 175
    health = 300
    recharge = 5
    reload = 1.5 * c.fps
    damage = 20

    def __init__(self, cell, projectiles):
        images, _ = get_images_from_sprite_sheet("assets/plants/snowPea.png",
                                                 7, 3, size=c.sizes["plant"])
        super().__init__(cell, anim_speed=c.fps // 20,
                         images=images)
        self.projectiles = projectiles
        self.shot_sound = pygame.mixer.Sound("assets/audio/throw.wav")

    def act(self):
        """
        Creates SnowProjectile object
        and adds it to the location projectiles group
        :return: None
        """
        b = SnowProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)
        self.shot_sound.play()
