import pygame
from pygame.locals import *


class Sprite(pygame.sprite.Sprite):

    def __init__(self, x, y, image=None, size=None):
        super().__init__()
        # Позиция изображения
        if image is not None:
            if size is not None:
                image = pygame.transform.scale(image, size)
            self.image = image
        else:
            self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def _draw(self, screen):
        """Метод, вызываемый внутри update
        Вывод изображение на экран"""
        screen.blit(self.image, self.rect)

    def update(self, screen):
        self._draw(screen)
