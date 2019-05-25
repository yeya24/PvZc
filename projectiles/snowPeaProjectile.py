import pygame

from config import fps, sizes
from .projectile import Projectile


class SnowProjectile(Projectile):
    freeze_time = fps * 1.5

    def __init__(self, x, y, row):
        self.sound = pygame.mixer.Sound("assets/audio/snow_pea_sparkles.wav")
        self.sound.play(-1)
        super().__init__(x + 5, y + 5, row,
                         6, 20,
                         pygame.image.load("assets/plants/snowPeaProjectile.png").
                         convert_alpha(),
                         size=sizes["projectile"])

    def kill(self):
        super().kill()
        self.sound.stop()
