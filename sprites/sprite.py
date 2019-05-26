import pygame


class Sprite(pygame.sprite.Sprite):
    """
    Extended pygame.sprite.Sprite class
    Has image or empty image if only size given
    Or loads image from given path
    Changes size of image if size is given
    Has rect with given x and y coordinates
    Which refer to the left top corner
    """

    def __init__(self, x: int, y: int,
                 image: pygame.Surface = None,
                 size: tuple = None, path: str = None):
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
        """
        Draws image on rect positions
        :param screen: Surface
        :return: None
        """
        screen.blit(self.image, self.rect)

    def update(self, screen):
        """
        Combined method
        Used to update object logic and call drawing
        :param screen: Surface
        :return: None
        """
        self._draw(screen)
