import pygame
from pygame.locals import *

from config import *
from sprite import Sprite

import random


def get_plant_card_path(plants):
    # Возвращает список с путями к изоюбражениям
    paths = []
    for plant in plants:
        paths.append(f"assets/images/card_{plant.__name__.lower()}.png")
    return paths


def get_transparent_image(image, alpha=128):
    im = image.copy()
    im.fill((255, 255, 255, alpha), None, BLEND_RGBA_MULT)
    return im


class TopMenu:
    def __init__(self, cards):
        # TODO добавить остальные цифры
        self.digits = {
            "1": pygame.image.load("assets/images/1.png").convert_alpha(),
            "2": pygame.image.load("assets/images/2.png").convert_alpha(),
            "5": pygame.image.load("assets/images/5.png").convert_alpha(),
            "7": pygame.image.load("assets/images/7.png").convert_alpha(),
            "0": pygame.image.load("assets/images/0.png").convert_alpha(),
        }

        frame = pygame.image.load("assets/images/topmenu.png").convert_alpha()
        self.frame = Sprite(100, 0, image=frame, size=tuple(sizes["topmenu"].values()))

        self.cards = pygame.sprite.Group()
        x = pads["menubar"]["x"] + pads["sun"]["x"]
        for path, plant in zip(get_plant_card_path(cards), cards):
            image = pygame.image.load(path).convert()
            s = Card(x, plant, image=image, size=tuple(sizes["card"].values()))
            self.cards.add(s)

            x += sizes["card"]["w"] + pads["cards"]

    def update(self, screen, sun):
        self.frame.update(screen)
        self.cards.update(screen)

        score_digits = list(map(lambda digit: self.digits[digit], str(sun)))
        digit_widths = list(map(lambda image: image.get_width(), score_digits))

        offset = pads["menubar"]["x"] + (pads["sun"]["x"] - sum(digit_widths)) // 2
        for image, width in zip(score_digits, digit_widths):
            screen.blit(image, (offset, pads["sun"]["y"]))
            offset += width

    def choose_card(self, mouse_pos, previous_choice):
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                choice = card.choose()
                # Отмена предыдущего выбора
                if choice == previous_choice:
                    return None
                return choice
        return previous_choice


class Card(Sprite):
    def __init__(self, x, plant, image, size=None):
        super().__init__(x, 8, image, size)
        self.plant = plant

    def choose(self):
        return self.plant


class Sun(Sprite):
    speedy = sun_speedY

    def __init__(self, x, y, max_y, sunflower=False):
        super().__init__(x, y,
                         image=pygame.image.load("assets/images/sun.png").convert_alpha(),
                         size=tuple(sizes["sun"].values()))

        self.despawn_time = fps * 20
        self.max_y = max_y
        self.speedx = 0
        if sunflower:
            self.up_go = (max_y - y) // self.speedy  # Поднимается до верхней границы клетки
            self.speedx = random.choice(sun_speedX)

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
