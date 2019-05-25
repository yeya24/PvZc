import random

import pygame
from pygame.locals import *

from config import fps, pads, sizes, XCells
from misc import lcm, transform_image
from sprites import Sprite


class Zombie(Sprite):
    """
    Complex base class for zombies
    """
    # Animation speed
    animation_frame = fps / 10
    counter = 0
    # Characteristics
    health = 200
    speed = 0.23
    damage = 100
    reload = fps

    groan = 9 * fps

    def __init__(self, row, images, size):
        super().__init__(
            sizes["win"][0],  # Right after the screen edge
            pads["game"][1] + (row - 3 / 4) * sizes["cell"][1],
            image=next(images), size=size
        )
        # Animation
        # Infinite iterator with images
        # So image update can be easily called with next func
        self.images = images
        # Real x pos, while rect x is floored
        self.x = self.rect.x
        # Target enemy plant
        self.eating = pygame.sprite.GroupSingle()
        # Freeze chars - makes walking and attacking slower
        self.frozen = False
        self.frozen_reload = self.reload * 2
        self.frozen_speed = self.speed / 2
        # After being shot makes nex image lighter
        self.shot = False
        # Game position
        self.col = XCells + 1
        self.row = row
        # Sounds
        self.chomps = [
            pygame.mixer.Sound("assets/audio/chomp.wav"),
            pygame.mixer.Sound("assets/audio/chomp2.wav"),
            pygame.mixer.Sound("assets/audio/chompsoft.wav")
        ]
        self.groans = [
            pygame.mixer.Sound("assets/audio/groan.wav"),
            pygame.mixer.Sound("assets/audio/groan2.wav"),
            pygame.mixer.Sound("assets/audio/groan3.wav"),
            pygame.mixer.Sound("assets/audio/groan4.wav"),
            pygame.mixer.Sound("assets/audio/groan5.wav"),
            pygame.mixer.Sound("assets/audio/groan6.wav"),

        ]
        self.frozen_sound = pygame.mixer.Sound("assets/audio/frozen.wav")
        self.frozen_sound.set_volume(0.6)
        random.choice(self.groans).play()

    def update(self, screen):
        """
        Called every tick
        Updates zombie

        Either makes zombie go or attack
        Regarding freeze caused py SnowPea's
        Which makes everything slower
        :param screen: pygame.display
        :return: None
        """
        self.counter += 1
        # Walk animation
        # Or damage infliction
        if self.counter % self.animation_frame == 0:
            self.image = next(self.images)
            # If zombie is frozen makes its image blue
            if self.frozen:
                self.frozen -= 1
                self.image = transform_image(self.image, r=0, g=0, b=128, alpha=5,
                                             special_flag=BLEND_RGBA_ADD)
            # If zombie is hit makes it lighter
            if self.shot:
                self.shot = False
                self.image = transform_image(self.image,
                                             r=64, g=64, b=64, alpha=5,
                                             special_flag=BLEND_RGBA_ADD)
        if not self.busy():  # If zombie is not eating
            # Movement
            if not self.frozen:
                self.x -= self.speed
            else:
                self.x -= self.frozen_speed
            self.rect.x = int(self.x) + 1
            # Using flooring because pygame rect doesn't support not-int coordinates
        else:
            # Damage infliction
            if (not self.frozen and self.counter % self.reload == 0) or \
                    (self.counter % self.frozen_reload == 0):
                random.choice(self.chomps).play()
                self.deal_damage()

        if self.counter % self.groan == 0:
            random.choice(self.groans).play()

        self.counter %= lcm(self.reload, self.animation_frame, self.groan)
        # Update cell on the game field
        self.col = (self.rect.x - pads["game"][0] + sizes["cell"][0] / 2) // sizes["cell"][0]
        self._draw(screen)

    def busy(self) -> bool:
        """
        Checks if zombie is eating anything
        :return: bool
        """
        return bool(len(self.eating))

    def coords(self) -> tuple:
        """
        Returns coordinates on the game field
        :return: (row, col)
        """
        return self.row, self.col

    def change_target(self, enemy):
        """
        Changes eating target on the given one
        :param enemy: Plant
        :return: None
        """
        self.eating.add(enemy)

    def check_alive(self):
        """
        Kills itself if health below or equals zero
        :return: None
        """
        if self.health <= 0:
            self.kill()

    def take_damage(self, bullet):
        """
        Takes damage from bullet and removes it
        Also makes self image blue if projectile.__class__ == SnowProjectile
        :param bullet: Projectile
        :return: None
        """
        bullet.deal_damage(self)
        self.check_alive()
        bullet.kill()

        if bullet.__class__.__name__ == "SnowProjectile":
            self.frozen = bullet.freeze_time
            # "Замораживает" зомби - делает изображение синим начиная с текущего
            self.image = transform_image(self.image, r=0, g=0, b=128, alpha=5,
                                         special_flag=BLEND_RGBA_ADD)
            self.frozen_sound.play()

        self.shot = True

    def deal_damage(self):
        """
        Lowers target plant health
        :return: None
        """
        self.eating.sprite.health -= self.damage
        self.eating.sprite.check_alive()