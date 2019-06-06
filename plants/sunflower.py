import pygame

import config as c
from misc import get_images_from_sprite_sheet
from sprites import Sun
from ._plant import _Plant


class Sunflower(_Plant):
    """
    Sunflower drops suns
    """
    shadow = pygame.image.load("assets/plants/sunflower_.png")

    sunCost = 50
    health = 300
    recharge = 5
    reload = c.fps * 24

    def __init__(self, cell, suns_group):
        images, size = get_images_from_sprite_sheet("assets/plants/sunflower.png",
                                                    18, 3, size=c.sizes["plant"])
        super().__init__(cell, anim_speed=c.fps // 20,
                         images=images)
        self.suns_group = suns_group
        self.counter = c.fps * 17  # First sun drop is faster

        self.sun_sound = pygame.mixer.Sound("assets/audio/throw.wav")

    def act(self):
        """
        Creates Sun object
        and adds it to the location projectiles group
        :return: None
        """
        self.suns_group.add(
            Sun(self.rect.x, self.rect.top, self.rect.centery, True)
        )
        self.sun_sound.play()
