import pygame

import config as c
from misc import get_images_from_sprite_sheet
from ._plant import _Plant


class CherryBomb(_Plant):
    """
    Cherry bomb explodes in the 3 cell diameter
    """
    shadow = pygame.image.load("assets/plants/cherryBomb_.png")

    sunCost = 150
    health = 200
    recharge = 35
    damage = 1800
    reload = c.fps

    @classmethod
    def get_shadow(cls):
        return cls.shadow

    def __init__(self, cell):
        images, size = get_images_from_sprite_sheet("assets/plants/cherryBomb.png",
                                                    6, 3, ratio=0.9)
        self.explosion, _ = get_images_from_sprite_sheet("assets/plants/cherryBombExplosion.png",
                                                         17, 1)
        super().__init__(cell, anim_speed=c.fps // 30,
                         images=images, size=size)
        self.explode_sound = pygame.mixer.Sound("assets/audio/cherrybomb.wav")

        self.armed = False

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)

        if self.health > 0 and self.counter >= self.reload:
            self.counter, self.armed = 0, True
        # End of explosion animation
        elif self.counter == 4 * 17:
            self.kill()

        self._draw(screen)

    def explode(self, *zombies):
        """
        Explodes - deals massive damage in 1 cell radius
        for a period of time displays explosion animation
        :param zombies: any iterator with Zombie objects
        :return: None
        """
        # Configure position
        self.rect.y -= 50
        self.rect.x += 30

        for zombie in zombies:
            zombie.ignite()
        # Start explosion animation
        self.animation_frame = 4
        self.images = self.explosion
        self.health = self.counter = 0
        self.explode_sound.play()
