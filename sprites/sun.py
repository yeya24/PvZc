import pygame

from config import fps, sizes
from misc import transform_image
from .sprite import Sprite


class Sun(Sprite):
    """
    Sun object which adds sun currency
     if has been clicked on
    """
    speedy = 1.5
    despawn = fps * 20
    destination = (168, 55)
    fly_time = fps

    def __init__(self, x: int, y: int, max_y: int, sunflower: bool = False):
        super().__init__(x, y,
                         image=pygame.image.load("assets/misc/sun.png").convert_alpha(),
                         size=sizes["sun"])

        self.despawn_time = self.despawn
        self.max_y = max_y
        self.speedx = self.up_go = 0
        self.angle = 0
        self.flying = False
        self.pickup_sound = pygame.mixer.Sound("assets/audio/points.wav")
        if sunflower:  # Make sun go up before going down
            self.up_go = (max_y - y) // self.speedy

    def _draw(self, screen):
        """
        Rotates and draws sun on the display
        :param screen: Surface
        """
        self.angle += 1
        self.angle %= 360
        image = pygame.transform.rotate(self.image, self.angle)
        c = self.rect.center
        self.rect = image.get_rect()
        self.rect.center = c
        # Make sun transparent after time
        image = transform_image(image=image,
                                alpha=255 if self.despawn_time > fps * 5 else
                                int(self.despawn_time / fps / 5 * 255))
        screen.blit(image, self.rect)

    def update(self, screen):
        """
        Changes position and rotates itself
        :param screen: Surface
        :return: None
        """
        if not self.flying:
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
        else:
            self.flying += 1
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.flying >= self.fly_time * 0.9:
                self.kill()
        self._draw(screen)

    def check_collision(self, coords: tuple) -> bool:
        """
        Checks if given coords intersect
        :param coords: (x, y)
        :return: bool
        """
        if self.rect.collidepoint(coords):
            # self.kill()
            self.pickup_sound.play()
            return True
        return False

    def fly(self):
        coords = self.rect.center
        dx = self.destination[0] - coords[0]
        dy = self.destination[1] - coords[1]
        self.speedx = dx // self.fly_time
        self.speedy = dy // self.fly_time
        self.flying = 1
