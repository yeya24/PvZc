import pygame

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

    def choose(self) -> type:
        """
        :return: plant choice type
        """
        self.sound.play()
        return self.plant
