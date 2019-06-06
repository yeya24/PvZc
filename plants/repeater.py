import pygame

import config as c
from misc import get_images_from_sprite_sheet, lcm
from ._plant import _Plant
from .peaShooter import PeaShooter


class Repeater(_Plant):
    """
    Repeater is better peashooter which shoots two peas in a row
    """
    shadow = pygame.image.load("assets/plants/repeater_.png")

    sunCost = 200
    health = 300
    recharge = 5
    reload = c.fps * 1.5
    damage = 20

    def __init__(self, cell, projectiles):
        images, _ = get_images_from_sprite_sheet("assets/plants/repeater.png",
                                                 14, 3, size=c.sizes["plant"])
        _Plant.__init__(self, cell, anim_speed=c.fps // 20,
                        images=images)
        self.projectiles = projectiles
        self.shot_sound = pygame.mixer.Sound("assets/audio/throw.wav")

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:  # First shot
            self.act()
        elif (self.counter - c.time_repeater_second_shot) % self.reload == 0:  # Second shot
            self.act()

        self.counter %= lcm(self.reload, self.reload + c.time_repeater_second_shot,
                            self.animation_frame)
        self._draw(screen)

    act = PeaShooter.act
