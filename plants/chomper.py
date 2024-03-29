import pygame

import config as c
from misc import get_images_from_sprite_sheet
from ._plant import _Plant


class Chomper(_Plant):
    shadow = pygame.image.load("assets/plants/chomper_.png")

    sunCost = 150
    health = 300
    recharge = 5
    reload = c.fps * 42

    def __init__(self, cell):
        images, _ = get_images_from_sprite_sheet("assets/plants/chomper.png",
                                                 31, 1, size=c.sizes["plant"])
        super().__init__(cell, anim_speed=2,
                         images=images)

        self.catching_animation, _ = get_images_from_sprite_sheet("assets/plants/chomperCatch.png",
                                                                  4, 5, ratio=0.75)
        self.eating_animation, _ = get_images_from_sprite_sheet("assets/plants/chomperEating.png",
                                                                6, 3, size=c.sizes["plant"])
        self.chop_sound = pygame.mixer.Sound("assets/audio/Bigchomp.ogg")
        self.eating = self.catching = self.reload_count = False
        self.target = None

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            if self.eating:
                # 2 is used to mark the first time eating
                if self.eating == 2:
                    self.rect.y += 35
                    self.eating = True
                self.image = next(self.eating_animation)
                # Wait for end of eating
                if self.reload_count:
                    self.reload_count -= 1
                    if self.reload_count == 0:
                        self.eating = False
            # Zombie catching animation
            elif self.catching:
                self.catching -= 1
                self.image = next(self.catching_animation)
                if self.catching == 10:
                    self.chop_sound.play()
                if self.catching == 0:
                    self.eating = 2
                    self.target.kill()

            else:  # Usual state
                self.image = next(self.images)

        self.counter %= self.animation_frame
        self._draw(screen)

    def catch(self, zombie):
        """
        Start of catching animation
        kills zombie after it
        :param zombie: Zombie
        :return: None
        """
        self.target = zombie
        self.catching = 20
        self.animation_frame = 3
        self.rect.y -= 35
        self.reload_count = self.reload

    def busy(self) -> bool:
        """
        Checks if Chomper is eating something
        :return: True if chomper eating
        """
        return self.eating or self.catching or self.reload_count
