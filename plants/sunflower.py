import pygame

from config import fps, sizes
from misc import get_images_from_sprite_sheet, lcm
from sprites import Sun
from .plant import Plant


class Sunflower(Plant):
    """
    Sunflower drops suns
    """
    shadow = pygame.image.load("assets/plants/sunflower_.png")

    sunCost = 50
    health = 300
    recharge = 5
    reload = fps * 24

    def __init__(self, cell, suns_group):
        images, size = get_images_from_sprite_sheet("assets/plants/sunflower.png",
                                                    18, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 20,
                         images=images, size=size)
        self.suns_group = suns_group
        self.counter = fps * 17

        self.sun_sound = pygame.mixer.Sound("assets/audio/throw.wav")

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
        Creates Sun object
        and adds it to the location projectiles group
        :return: None
        """
        self.suns_group.add(
            Sun(self.rect.x, self.rect.top, self.rect.centery, True)
        )
        self.sun_sound.play()
