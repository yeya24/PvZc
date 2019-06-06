import pygame

import config as c
from misc import get_images_from_sprite_sheet
from projectiles import PeashooterProjectile
from ._plant import _Plant


class PeaShooter(_Plant):
    """
    The most basic plant which shoots peas
    """
    shadow = pygame.image.load("assets/plants/peaShooter_.png")

    sunCost = 100
    health = 300
    recharge = 5
    damage = 20
    reload = c.fps * 1.5

    def __init__(self, cell, projectiles: pygame.sprite.Group):
        images, size = get_images_from_sprite_sheet("assets/plants/peaShooter.png",
                                                    13, 3, size=c.sizes["plant"])
        super().__init__(cell, anim_speed=c.fps // 30,
                         images=images, size=size)
        self.projectiles = projectiles

        self.shot_sound = pygame.mixer.Sound("assets/audio/throw.wav")

    def act(self):
        """
        Creates PeashooterBullet object
        and adds it to the location projectiles group
        :return: None
        """
        b = PeashooterProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)
        self.shot_sound.play()
