import pygame

from sprite import Sprite
import random

from config import sizes, fps


class Projectile(Sprite):
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
        target.health -= self.damage
        random.choice(self.hit_sounds).play()

    def update(self, screen):
        self.rect.x += self.speed
        self._draw(screen)
        if self.rect.x >= sizes["win"][0]:
            self.kill()


class PeashooterProjectile(Projectile):
    def __init__(self, x, y, row):
        super().__init__(x + 5, y + 5, row,
                         6, 20,
                         pygame.image.load("assets/images/peaShooterProjectile.png").
                         convert_alpha(),
                         size=sizes["projectile"])


class SnowProjectile(Projectile):
    freeze_time = fps * 1.5

    def __init__(self, x, y, row):
        self.sound = pygame.mixer.Sound("assets/audio/snow_pea_sparkles.wav")
        self.sound.play(-1)
        super().__init__(x + 5, y + 5, row,
                         6, 20,
                         pygame.image.load("assets/images/snowPeaProjectile.png").
                         convert_alpha(),
                         size=sizes["projectile"])

    def kill(self):
        super().kill()
        self.sound.stop()
