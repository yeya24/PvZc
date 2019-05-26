import random

import pygame

from config import sizes
from sprites import Sprite


class Projectile(Sprite):
    """
    Base class for pea shooting plants' projectiles
    """
    def __init__(self, x: int, y: int, row: int,
                 speed: float, damage: int,
                 image: pygame.Surface, size: tuple = None):
        super().__init__(x, y, image, size)
        self.speed = speed
        self.damage = damage
        self.row = row
        self.hit_sounds = [
            pygame.mixer.Sound("assets/audio/splat2.wav"),
            pygame.mixer.Sound("assets/audio/splat3.wav"),
        ]

    def deal_damage(self, target):
        """
        Lowers enemy health
        :param target: Zombie
        :return: None
        """
        target.health -= self.damage
        random.choice(self.hit_sounds).play()

    def update(self, screen):
        """
        Moves right and draws image
        :param screen: Surface
        :return: None
        """
        self.rect.x += self.speed
        self._draw(screen)
        if self.rect.x >= sizes["win"][0]:
            self.kill()
