import pygame

from config import fps, sizes
from misc import get_images_from_sprite_sheet, lcm
from projectiles import PeashooterProjectile
from .plant import Plant


class Repeater(Plant):
    """
    Repeater is better peashooter which shoots two peas in a row
    """
    shadow = pygame.image.load("assets/plants/repeater_.png")

    sunCost = 200
    health = 300
    recharge = 5
    reload = fps * 1.5
    damage = 20

    def __init__(self, cell, projectiles):
        images, size = get_images_from_sprite_sheet("assets/plants/repeater.png",
                                                    14, 3, size=sizes["plant"])
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
        elif (self.counter - 10) % self.reload == 0:
            self.shot()

        self.counter %= lcm(self.reload, self.reload + 10, self.animation_frame)
        self._draw(screen)

    def shot(self):
        b = PeashooterProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)
        self.shot_sound.play()
