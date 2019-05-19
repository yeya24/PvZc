import pygame


class Sprite(pygame.sprite.Sprite):

    def __init__(self, x, y, image=None, size=None, path=None):
        super().__init__()
        if image is not None:
            if size is not None:
                image = pygame.transform.smoothscale(image, size)
            self.image = image
        elif path is not None:
            self.image = pygame.image.load(path)
        elif size is not None:
            self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def _draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, screen):
        self._draw(screen)
