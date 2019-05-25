import pygame

from config import fps, sizes
from .sprite import Sprite


class Sun(Sprite):
    """
    Sun object which adds sun currency
     if has been clicked on
    """
    speedy = 1.5
    angle = 0

    def __init__(self, x: int, y: int, max_y: int, sunflower: bool = False):
        super().__init__(x, y,
                         image=pygame.image.load("assets/misc/sun.png").convert_alpha(),
                         size=sizes["sun"])

        self.despawn_time = fps * 20
        self.max_y = max_y
        self.speedx = self.up_go = 0
        self.pickup_sound = pygame.mixer.Sound("assets/audio/points.wav")
        if sunflower:  # Make sun go up before going down
            self.up_go = (max_y - y) // self.speedy

    def update(self, screen):
        """
        Changes position and rotates itself
        :param screen: pygame.display
        :return: None
        """
        if self.up_go:
            self.up_go -= 1
            self.rect.y -= self.speedy
            self.rect.x += self.speedx

        elif self.rect.y < self.max_y:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
        else:
            self.despawn_time -= 1
            if self.despawn_time < 0:
                self.kill()

        self._draw(screen)

    def check_collision(self, coords: tuple) -> bool:
        """
        Checks if given coords intersect
        :param coords: (x, y)
        :return: bool
        """
        if self.rect.collidepoint(coords):
            self.kill()
            self.pickup_sound.play()
            return True
        return False

    def _draw(self, screen):
        """
        Rotates and draws sun on the display
         :param screen: pygame.display
        """
        self.angle += 1
        self.angle %= 360
        image = pygame.transform.rotate(self.image, self.angle)
        c = self.rect.center
        self.rect = image.get_rect()
        self.rect.center = c
        screen.blit(image, self.rect)
