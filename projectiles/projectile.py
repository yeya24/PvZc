import random

import pygame

from config import sizes
from sprites import Sprite


class Projectile(Sprite):
    def __init__(self, x: int, y: int, row: int,
                 speed: float, damage: int,
                 image: pygame.Surface, size: tuple = None):
        super().__init__(x, y, image, size)
        self.speed = speed
        self.damage = damage
        self.row = row
        self.hit_sounds = [
            pygame.mixer.Sound("audio/splat2.wav"),
            pygame.mixer.Sound("audio/splat3.wav"),
        ]

    def deal_damage(self, target):
        target.health -= self.damage
        random.choice(self.hit_sounds).play()

    def update(self, screen):
        self.rect.x += self.speed
        self._draw(screen)
        if self.rect.x >= sizes["win"][0]:
            self.kill()
