from .plant import Plant
import pygame
from misc import get_images_from_sprite_sheet
from config import sizes, fps


class CherryBomb(Plant):
    """
    Cherry bomb explodes in the 3 cell diameter
    """
    shadow = pygame.image.load("assets/plants/cherryBomb_.png")

    sunCost = 150
    health = 200
    recharge = 35
    damage = 1800
    reload = fps

    def __init__(self, cell):
        images, size = get_images_from_sprite_sheet("assets/plants/cherryBomb.png",
                                                    0, 0, size=sizes["plant"])
        super().__init__(cell, anim_speed=fps // 30,
                         images=images, size=size)
        self.explode_sound = pygame.mixer.Sound("assets/audio/cherrybomb.wav")
        self.explosion = pygame.image.load("assets/plants/cherryBombExplosion.png").convert_alpha()
        self.exploded = False

    def update(self, screen):
        self.counter += 1
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
        if self.counter == self.reload:
            self.exploded = True
        elif self.counter == self.reload + 120:
            self.kill()
        self._draw(screen)

    def explode(self, *zombies):
        dx = self.explosion.get_width() - self.image.get_width()
        dy = self.explosion.get_height() - self.image.get_height()
        self.rect.x += dx
        self.rect.y += dy
        self.image = self.explosion
        for zombie in zombies:
            zombie.health -= self.damage
            zombie.check_alive()
