import pygame

from config import pads, sizes
from sprites import Sprite
from .card import Card


class TopMenu:
    """
    Class for handling menu on the top
    Which includes sun score indicator
    Plant card choices
    And shovel
    """

    def __init__(self, cards: list = None, pos: int = 100):
        if cards is None:
            cards = []
        # TODO добавить остальные цифры
        # Digits for sun display
        self.digits = {
            "1": pygame.image.load("assets/misc/1.png").convert_alpha(),
            "2": pygame.image.load("assets/misc/2.png").convert_alpha(),
            "5": pygame.image.load("assets/misc/5.png").convert_alpha(),
            "7": pygame.image.load("assets/misc/7.png").convert_alpha(),
            "0": pygame.image.load("assets/misc/0.png").convert_alpha(),
        }
        # Main frame
        self.frame = Sprite(pos, 0,
                            image=pygame.image.load("assets/misc/topmenu.png").convert_alpha(),
                            size=sizes["topmenu"])
        # Positions cards
        self.cards = pygame.sprite.Group()
        self.x = pads["sun"][0] + (pads["menubar"][0] if pos == 100 else 0)
        self.starting_x = self.x
        for card in cards:
            image = pygame.image.load(f"assets/cards/card{card.__name__}.png").convert()
            s = Card(self.x, card, image=image, size=sizes["card"])
            self.cards.add(s)
            self.x += sizes["card"][0] + pads["cards"]

    def update(self, screen, sun: int):
        """
        Updates all parts of the interface
        :param screen: pygame.display
        :param sun: sun count int
        :return: None
        """
        self.frame.update(screen)
        self.cards.update(screen)

        # score_digits = list(map(lambda digit: self.digits[digit], str(sun)))
        # digit_widths = list(map(lambda image: image.get_width(), score_digits))
        #
        # offset = pads["menubar"][0] + (pads["sun"][0] - sum(digit_widths)) // 2
        # for image, width in zip(score_digits, digit_widths):
        #     screen.blit(image, (offset, pads["sun"][1]))
        #     offset += width

    def choose_card(self, mouse_pos: tuple, previous_choice: type) -> type:
        """
        Checks mouse position on intersections with cards
        Changes choice or deletes it if clicked the same card
        :param mouse_pos: (x, y)
        :param previous_choice: plant type
        :return: plant type or None
        """
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                choice = card.choose()
                # Last choice deletion
                if choice == previous_choice:
                    return None
                return choice
        return previous_choice

    def add_card(self, plant: type):
        if any(filter(lambda card: card.plant == plant, self.cards)):
            return
        s = Card(self.x,
                 image=pygame.image.load(f"assets/cards/card{plant.__name__}.png").convert(),
                 size=sizes["card"], plant=plant)
        self.x += sizes["card"][0] + pads["cards"]
        self.cards.add(s)

    def remove_card(self, mouse_pos: tuple):
        """
        Removes clicked card and moves other to the left
        :param mouse_pos: (x, y)
        :return:
        """
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                self.cards.remove(card)
                x = self.starting_x
                for card in self.cards:
                    card.rect.x = x
                    x += sizes["card"][0] + pads["cards"]
                self.x = x
                return

    def move_right(self):
        dx = pads["menubar"][0]

        self.x += dx
        for card in self.cards:
            card.rect.x += dx
        self.frame.rect.x += dx
