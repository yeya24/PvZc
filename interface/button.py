import pygame

from sprite import Sprite


class Button(Sprite):
    """
    Simple class defining buttons
    """

    def __init__(self, x, y, im1, im2, size=None):
        if size is not None:
            im1 = pygame.transform.smoothscale(im1, size)
            im2 = pygame.transform.smoothscale(im2, size)
        super().__init__(x, y, im1)
        self.im1 = im1
        self.im2 = im2

    def update(self, screen, mouse_pos):
        """
        Checks if mouse if on button
        and draws image
        :param screen: Surface
        :param mouse_pos: (x, y)
        :return: None
        """
        image = self.im1
        if self.click(mouse_pos):
            image = self.im2
        screen.blit(image, self.rect)

    def click(self, mouse_pos) -> bool:
        x, y = mouse_pos
        if self.rect.collidepoint(mouse_pos):
            if self.image.get_at((x - self.rect.x, y - self.rect.y))[3]:
                return True
        return False
