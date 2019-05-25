import pygame

from config import sizes
from .projectile import Projectile


class PeashooterProjectile(Projectile):
    def __init__(self, x, y, row):
        super().__init__(x + 5, y + 5, row,
                         6, 20,
                         pygame.image.load("assets/plants/peaShooterProjectile.png").
                         convert_alpha(),
                         size=sizes["projectile"])
