import pygame

import config as c
from ._projectile import _Projectile


class PeashooterProjectile(_Projectile):
    """
    Usual green projectile that deals 20 damage
    """

    def __init__(self, x: int, y: int, row: int):
        super().__init__(x + 5, y + 5, row,
                         6, 20,
                         pygame.image.load("assets/plants/peaShooterProjectile.png").
                         convert_alpha(),
                         size=c.sizes["projectile"])
