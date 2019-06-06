import pygame

import config as c
from .sprite import Sprite


class LawnMower(Sprite):
    """
    Lawn Mower class
    Which stay still on the lift side of the field
    and run and kill everything on the line if zombie comes close to the house
    """
    speedX = 3

    def __init__(self, row: int):
        image = pygame.image.load("assets/misc/lawnMover.png").convert_alpha()
        super().__init__(
            c.pads["game"][0] - image.get_width() / 2,
            c.pads["game"][1] + c.sizes["cell"][1] * (row + 1 / 4),
            image=image, size=c.sizes["lawnmover"]
        )
        self.row = row
        self.running = False
        self.sound = pygame.mixer.Sound("assets/audio/lawnmower.wav")

    def update(self, screen) -> bool:
        """
        Changes position if running
        Returns True if is out of window bounds
        :param screen: Surface
        :return : bool
        """
        if self.running:
            if self.rect.x > c.sizes["win"][0]:
                return True

            self.rect.x += self.speedX
        self._draw(screen)
        return False

    def run(self):
        """
        Start going right and slaughter zombies
        :return: None
        """
        self.sound.play()
        self.running = True
