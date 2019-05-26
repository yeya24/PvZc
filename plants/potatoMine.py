import pygame

from config import fps, sizes
from misc import get_images_from_sprite_sheet
from .plant import Plant


class PotatoMine(Plant):
    """
    Potato mine explodes with giant damage
     after being armed for several seconds
    """
    shadow = pygame.image.load("assets/plants/potatoMine_.png")

    sunCost = 25
    health = 300
    recharge = 20
    damage = 1800
    reload = fps * 14

    def __init__(self, cell):
        self.images, _ = get_images_from_sprite_sheet("assets/plants/potatoMineReady.png",
                                                      7, 4)
        self.arming, size = get_images_from_sprite_sheet("assets/plants/potatoMineArming.png",
                                                         1, 3, size=sizes["plant"], cycle=False)
        self.explosion = pygame.transform.smoothscale(
            pygame.image.load("assets/plants/potatoMineExplosion.png").convert_alpha(),
            sizes["potatoExp"])
        super().__init__(cell,
                         anim_speed=fps // 12,
                         image=self.arming[0],
                         size=size)
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
        self.rect.x -= (sizes["potatoExp"][0] - sizes["cell"][0]) // 2
        self.rect.y -= (sizes["potatoExp"][1] - sizes["cell"][1]) // 1.2
        enemy.health -= self.damage
        enemy.check_alive()
        self.health = 0  # Start displaying explosion
        self.detonation_sound.play()
