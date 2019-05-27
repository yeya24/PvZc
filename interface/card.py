import pygame

from config import fps
from misc import greyscale
from sprites import Sprite


class Card(Sprite):
    """
    Class which keeps plant type
    and card image
    """

    def __init__(self, x: int, plant: type,
                 image: pygame.Surface, size: tuple = None, y: int = 8):
        super().__init__(x, y, image, size)
        self.plant = plant
        # Plant choice sound
        self.sound = pygame.mixer.Sound("assets/audio/seedlift.wav")
        self.negative = greyscale(self.image)
        self.counter = 0

    def update(self, screen, sun):

        if self.counter:
            self.counter -= 1
            neg = self.negative.copy()
            y = int(self.image.get_height() * (self.counter / (self.plant.recharge * fps)))
            rect = (0, y, self.image.get_width(), self.image.get_height() - y)
            col = pygame.Surface((rect[2], rect[3]))
            col.blit(self.image, (rect[0], -rect[1]))
            neg.blit(col, rect)
            screen.blit(neg, self.rect)
        elif sun >= self.plant.sunCost:
            self._draw(screen)
        else:
            screen.blit(self.negative, self.rect)

    def choose(self) -> type:
        """
        :return: plant choice type
        """
        if not self.counter:
            self.sound.play()
            return self.plant

    def set_timer(self):
        self.counter = self.plant.recharge * fps
