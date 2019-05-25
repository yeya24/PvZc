import pygame

from config import fps, sizes
from misc import get_images_from_sprite_sheet
from .plant import Plant


class Chomper(Plant):
    shadow = pygame.image.load("assets/plants/chomper_.png")

    sunCost = 150
    health = 300
    recharge = 5
    reload = fps * 42

    def __init__(self, cell):
        images, size = get_images_from_sprite_sheet("assets/plants/chomper.png",
                                                    31, 1, size=sizes["plant"])
        super().__init__(cell, anim_speed=2,
                         images=images, size=size)

        self.catching_animation, _ = get_images_from_sprite_sheet("assets/plants/chomperCatch.png",
                                                                  4, 5, ratio=0.75)
        self.eating_animation, _ = get_images_from_sprite_sheet("assets/plants/chomperEating.png",
                                                                6, 3, size=sizes["plant"])
        self.chop_sound = pygame.mixer.Sound("assets/audio/Bigchomp.ogg")
        self.eating = self.catching = self.reload_count = False
        self.target = None

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            if self.eating:

                if self.eating == 2:
                    self.rect.y += 35
                    self.eating = True
                self.image = next(self.eating_animation)

                if self.reload_count:
                    self.reload_count -= 1
                    if self.reload_count == 0:
                        self.eating = False

            elif self.catching:
                self.animation_frame = 3
                self.catching -= 1
                self.image = next(self.catching_animation)

                if self.catching == 0:
                    self.eating = 2
                    self.target.kill()
            else:
                self.image = next(self.images)

        self.counter %= self.animation_frame
        self._draw(screen)

    def catch(self, zombie):
        self.target = zombie
        self.catching = 20
        self.rect.y -= 35
        self.reload_count = self.reload

    def busy(self) -> bool:
        return self.eating or self.catching or self.reload_count
