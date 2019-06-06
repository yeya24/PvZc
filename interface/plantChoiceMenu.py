import pygame

import config as c
from sprites import Sprite
from .card import Card


class PlantChoiceMenu:
    def __init__(self, cards):
        self.frame = Sprite(0, c.sizes["topmenu"][1],
                            image=pygame.image.load(
                                "assets/misc/chooseYourPlants.png").convert_alpha(),
                            size=c.sizes["choose"])
        self.button_images = list(
            map(lambda i: pygame.transform.smoothscale(i, c.sizes["letsRock"]), [
                pygame.image.load("assets/misc/letsRock.png").convert_alpha(),
                pygame.image.load("assets/misc/letsRockHighlight.png").convert_alpha()
            ])
        )
        self.button = Sprite(158, 568, image=self.button_images[0])

        self.cards = pygame.sprite.Group()
        self.x = c.pads["choose"][0]
        self.starting_x = self.x
        y = c.pads["choose"][1]
        _c = 0
        for card in cards:
            _c += 1
            image = pygame.image.load(f"assets/cards/card{card.__name__}.png").convert()
            s = Card(self.x, card, image=image, size=c.sizes["card"], y=y)
            self.cards.add(s)
            self.x += c.sizes["card"][0] + 2
            if _c % 7 == 0:
                self.x = self.starting_x
                y += c.sizes["card"][1] + 5

    def update(self, screen, mouse_pos):
        """
        :param screen: Surface
        :param mouse_pos: (x, y)
        :return:
        """
        # Marks the Let's Rock button if mouse collides with it
        if self.button.rect.collidepoint(mouse_pos):
            self.button.image = self.button_images[1]
        else:
            self.button.image = self.button_images[0]

        self.frame.update(screen)
        self.button.update(screen)
        self.cards.update(screen, float("inf"))

    def choose_card(self, mouse_pos: tuple) -> type:
        """
        Checks mouse position on intersections with cards
        Returns choice or None
        :param mouse_pos: (x, y)
        :return: plant type or None
        """
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                choice = card.choose()
                return choice

    def button_click(self, mouse_pos: tuple) -> bool:
        return self.button.rect.collidepoint(mouse_pos)
