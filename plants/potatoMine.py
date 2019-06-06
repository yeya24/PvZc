import pygame

import config as c
from misc import get_images_from_sprite_sheet
from ._plant import _Plant


class PotatoMine(_Plant):
    """
    Potato mine explodes with giant damage
     after being armed for several seconds
    """
    shadow = pygame.image.load("assets/plants/potatoMine_.png")

    sunCost = 25
    health = 300
    recharge = 20
    damage = 1800
    reload = c.fps * 14

    def __init__(self, cell):
        self.images, _ = get_images_from_sprite_sheet("assets/plants/potatoMineReady.png",
                                                      7, 4)
        self.arming, _ = get_images_from_sprite_sheet("assets/plants/potatoMineArming.png",
                                                      1, 3, size=c.sizes["plant"], cycle=False)
        self.explosion = pygame.transform.smoothscale(
            pygame.image.load("assets/plants/potatoMineExplosion.png").convert_alpha(),
            c.sizes["potatoExp"])
        super().__init__(cell,
                         anim_speed=c.fps // 12,
                         image=self.arming[0])
        self.armed = False
        self.detonation = 60
        self.detonation_sound = pygame.mixer.Sound("assets/audio/potato_mine.wav")

    def update(self, screen):
        if self.health > 0:
            self.counter += 1
            if not self.armed:
                if self.counter == self.reload:
                    self.image = next(self.images)
                    self.counter, self.armed = 0, True

                elif self.counter > self.reload * 2 // 3:
                    self.image = self.arming[2]
                elif self.counter > self.reload // 3:
                    self.image = self.arming[1]

            elif self.counter == self.animation_frame:
                self.image = next(self.images)
                self.counter = 0
        else:
            self.detonation -= 1
            if not self.detonation:
                self.kill()
        self._draw(screen)

    def explode(self, enemy):
        """
        Deals damage to zombie
         and displays explosion image
        :param enemy: Zombie
        :return: None
        """
        self.image = self.explosion
        # Configure image position
        self.rect.x -= (c.sizes["potatoExp"][0] - c.sizes["cell"][0]) // 2
        self.rect.y -= (c.sizes["potatoExp"][1] - c.sizes["cell"][1]) // 1.2
        enemy.health -= self.damage
        enemy.check_alive()
        self.health = 0  # Start displaying explosion
        self.detonation_sound.play()
