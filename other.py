import pygame

from config import *
from sprite import Sprite


def lcm(*args) -> int:
    import math
    from functools import reduce
    return reduce(lambda a, b: a * b // math.gcd(a, b), map(int, args))


class TopMenu:
    def __init__(self, cards: list):
        # TODO добавить остальные цифры
        self.digits = {
            "1": pygame.image.load("assets/images/1.png").convert_alpha(),
            "2": pygame.image.load("assets/images/2.png").convert_alpha(),
            "5": pygame.image.load("assets/images/5.png").convert_alpha(),
            "7": pygame.image.load("assets/images/7.png").convert_alpha(),
            "0": pygame.image.load("assets/images/0.png").convert_alpha(),
        }

        frame = pygame.image.load("assets/images/topmenu.png").convert_alpha()
        self.frame = Sprite(100, 0, image=frame, size=sizes["topmenu"])

        self.cards = pygame.sprite.Group()
        x = pads["menubar"][0] + pads["sun"][0]
        for card in cards:
            image = pygame.image.load(f"assets/images/card{card.__name__}.png").convert()
            s = Card(x, card, image=image, size=sizes["card"])
            self.cards.add(s)

            x += sizes["card"][0] + pads["cards"]

    def update(self, screen, sun: int):
        self.frame.update(screen)
        self.cards.update(screen)

        # score_digits = list(map(lambda digit: self.digits[digit], str(sun)))
        # digit_widths = list(map(lambda image: image.get_width(), score_digits))
        #
        # offset = pads["menubar"][0] + (pads["sun"][0] - sum(digit_widths)) // 2
        # for image, width in zip(score_digits, digit_widths):
        #     screen.blit(image, (offset, pads["sun"][1]))
        #     offset += width

    def choose_card(self, mouse_pos: tuple, previous_choice: type):
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                choice = card.choose()
                # Отмена предыдущего выбора
                if choice == previous_choice:
                    return None
                return choice
        return previous_choice


class Card(Sprite):
    def __init__(self, x: int, plant: type,
                 image: pygame.Surface, size: tuple = None):
        super().__init__(x, 8, image, size)
        self.plant = plant
        # Звук выбора растения
        self.sound = pygame.mixer.Sound("assets/audio/seedlift.wav")

    def choose(self) -> type:
        self.sound.play()
        return self.plant


class Sun(Sprite):
    speedy = sun_speedY

    def __init__(self, x: int, y: int, max_y: int, sunflower: bool = False):
        super().__init__(x, y,
                         image=pygame.image.load("assets/images/sun.png").convert_alpha(),
                         size=sizes["sun"])

        self.despawn_time = fps * 20
        self.max_y = max_y
        self.speedx = self.up_go = 0
        self.pickup_sound = pygame.mixer.Sound("assets/audio/points.wav")
        if sunflower:
            self.up_go = (max_y - y) // self.speedy  # Поднимается до верхней границы клетки

    def update(self, screen):
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
        if self.rect.collidepoint(coords):
            self.kill()
            self.pickup_sound.play()
            return True
        return False


class LawnMover(Sprite):
    pass


class StageIndicator(Sprite):
    pass


class MenuButton(Sprite):
    pass
