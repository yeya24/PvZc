import pygame

from config import pads, sizes
from sprites import Sprite
from .card import Card


class PlantChoiceMenu:
    def __init__(self, cards):
        self.frame = Sprite(0, sizes["topmenu"][1],
                            image=pygame.image.load(
                                "assets/misc/chooseYourPlants.png").convert_alpha(),
                            size=sizes["choose"])
        self.button_images = list(
            map(lambda image: pygame.transform.smoothscale(image, sizes["letsRock"]), [
                pygame.image.load("assets/misc/letsRock.png").convert_alpha(),
                pygame.image.load("assets/misc/letsRockHighlight.png").convert_alpha()
            ])
        )
        self.button = Sprite(158, 568, image=self.button_images[0])

        # TODO make several layers support
        self.cards = pygame.sprite.Group()
        self.x = pads["choose"][0]
        for card in cards:
            image = pygame.image.load(f"assets/cards/card{card.__name__}.png").convert()
            s = Card(self.x, card, image=image, size=sizes["card"], y=pads["choose"][1])
            self.cards.add(s)
            self.x += sizes["card"][0] + 1

    def update(self, screen, mouse_pos):
        if self.button.rect.collidepoint(mouse_pos):
            self.button.image = self.button_images[1]
        else:
            self.button.image = self.button_images[0]

        self.frame.update(screen)
        self.button.update(screen)
        self.cards.update(screen)

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
