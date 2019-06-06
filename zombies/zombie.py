import random

import pygame
from pygame.locals import *

import config as c
from misc import get_images_from_sprite_sheet, lcm, transform_image
from sprites import Sprite


class Zombie(Sprite):
    """
    Complex base class for zombies
    """
    # Animation speed
    animation_frame = c.fps / 10
    counter = 0
    # Characteristics
    health = 200
    speed = 0.23
    damage = 100
    reload = c.fps

    groan = 9 * c.fps

    def __init__(self, row, images, size=None):
        super().__init__(
            c.sizes["win"][0],  # Right after the screen edge
            c.pads["game"][1] + (row - 3 / 4) * c.sizes["cell"][1],
            image=next(images), size=size
        )
        # --------------Animation--------------
        # Burn animation
        self.ignited, _ = get_images_from_sprite_sheet("assets/zombies/incinerated.png",
                                                       6, 5, size=c.sizes["zombie"])
        self.incinerated = False
        # Infinite iterator with images
        # So image update can be easily called with next() func
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
        self.col = c.XCells + 1
        self.row = row
        # --------------Sounds--------------
        self.chomps = (
            pygame.mixer.Sound("assets/audio/chomp.wav"),
            pygame.mixer.Sound("assets/audio/chomp2.wav"),
            pygame.mixer.Sound("assets/audio/chompsoft.wav")
        )
        self.groans = (
            pygame.mixer.Sound("assets/audio/groan.wav"),
            pygame.mixer.Sound("assets/audio/groan2.wav"),
            pygame.mixer.Sound("assets/audio/groan3.wav"),
            pygame.mixer.Sound("assets/audio/groan4.wav"),
            pygame.mixer.Sound("assets/audio/groan5.wav"),
            pygame.mixer.Sound("assets/audio/groan6.wav"),
        )
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
        # Placed separately not to over complicate if/else statements
        if self.incinerated:
            self.incinerated -= 1
            if self.incinerated % self.animation_frame == 0:
                self.image = next(self.ignited)
            self._draw(screen)
            if self.incinerated == 0:
                self.kill()
            return

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
        self.col = int((self.rect.x - c.pads["game"][0] + c.sizes["cell"][0] / 2)
                       // c.sizes["cell"][0])
        self._draw(screen)

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
            # Freezes zombie
            self.image = transform_image(self.image, r=0, g=0, b=128, alpha=5,
                                         special_flag=BLEND_RGBA_ADD)
            self.frozen_sound.play()

        self.shot = True

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

    def deal_damage(self):
        """
        Lowers target plant health
        :return: None
        """
        self.eating.sprite.take_damage(self.damage)

    def ignite(self):
        """
        Plays ignite animation and dies after
        Needed as kill animation for CherryBomb
        :return: None
        """
        self.incinerated = self.animation_frame * 30
