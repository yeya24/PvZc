import pygame

from config import fps, sizes
from misc import get_images_from_sprite_sheet, lcm
from projectiles import PeashooterProjectile
from .plant import Plant


class PeaShooter(Plant):
    """
    The most basic plant which shoots peas
    """
    shadow = pygame.image.load("assets/plants/peaShooter_.png")

    sunCost = 100
    health = 300
    recharge = 5
    damage = 20
    reload = fps * 1.5

    def __init__(self, cell, projectiles: pygame.sprite.Group):
        images, size = get_images_from_sprite_sheet("assets/plants/peaShooter.png",
                                                    13, 3, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 30,
                         images=images, size=size)
        self.projectiles = projectiles

        self.shot_sound = pygame.mixer.Sound("assets/audio/throw.wav")

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter % self.reload == 0:
            self.shot()

        self.counter %= lcm(self.reload * self.animation_frame)
        self._draw(screen)

    def shot(self):
        b = PeashooterProjectile(*self.rect.midtop, self.coords[0])
        self.projectiles.add(b)
        self.shot_sound.play()
