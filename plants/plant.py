import pygame
from pygame.locals import *

from config import sizes
from misc import transform_image
from sprites import Sprite


class Plant(Sprite):
    """
    Base plant class
    """
    counter = 0
    # Image which is displayed when plant is chosen to plant
    shadow = None
    # Characteristics
    sunCost = 100
    health = 300
    recharge = 5
    reload = 0
    damage = 0

    def __init__(self, cell, anim_speed: int = None,
                 images: list = None, image: pygame.Surface = None,
                 size: tuple = None):
        if images is None and image is None:
            image = pygame.Surface(size)
        elif images is not None:
            self.images = images
            image = next(images)
        # Positioning in the middle of the cell
        super().__init__(cell.rect.x + (sizes["cell"][0] - size[0]) / 2,
                         cell.rect.y + (sizes["cell"][1] - size[1]) / 2,
                         image=image, size=size)
        # Animations speed
        self.animation_frame = anim_speed

        self.row = cell.row
        self.col = cell.col
        self.coords = cell.coords
        self.next_white = True
        # Sound of being eaten by zombie
        self.death_sound = pygame.mixer.Sound("assets/audio/gulp.wav")

    def check_alive(self):
        """
        Kills itself if health if below of equals zero
        :return: None
        """
        if self.health <= 0:
            self.kill()
            self.death_sound.play()

    def _draw(self, screen):
        image = self.image
        if self.next_white:
            image = transform_image(image,
                                    r=64, g=64, b=64, alpha=5,
                                    special_flag=BLEND_RGBA_ADD)
            self.next_white -= 1
        screen.blit(image, self.rect)

    def update(self, screen):
        """
        Makes plant act and draws it
        :param screen: Surface
        :return: None
        """
        pass

    def take_damage(self, damage: int):
        """
        Take damage and set next several frames image more white
        :param damage:
        :return:
        """
        self.health -= damage
        self.next_white = 10
        self.check_alive()

    @classmethod
    def get_shadow(cls):
        """
        Returns converted and resized image
        :return: Surface
        """
        return pygame.transform.smoothscale(cls.shadow.convert_alpha(), sizes["plant"])
