import pygame

from config import pads, sizes
from .sprite import Sprite


class LawnMower(Sprite):
    """
    Lawn mover class
    Which stay still on the lift side of the field
    and run and kill everything on the line if zombie comes close to the house
    """
    speedX = 3

    def __init__(self, row: int):
        image = pygame.image.load("assets/misc/lawnMover.png").convert_alpha()
        super().__init__(
            pads["game"][0] - image.get_width() / 2,
            pads["game"][1] + sizes["cell"][1] * (row + 1 / 4),
            image=image, size=sizes["lawnmover"]
        )
        self.row = row
        self.running = False
        self.sound = pygame.mixer.Sound("assets/audio/lawnmower.wav")

    def update(self, screen) -> bool:
        """
        Changes position if running
        Returns True if is out of window bounds
        :param screen: pygame.display
        :return : bool
        """
        if self.running:
            if self.rect.x > sizes["win"][0]:
                return True

            self.rect.x += self.speedX
        self._draw(screen)
        return False

    def run(self):
        self.sound.play()
        self.running = True
