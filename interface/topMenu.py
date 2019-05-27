import pygame

from config import pads, sizes
from sprites import Sprite, Shovel
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
            str(n): pygame.image.load(f"assets/misc/{n}.png").convert_alpha() for n in range(10)
        }
        # Main frame
        self.frame = Sprite(pos, 0,
                            image=pygame.image.load("assets/misc/topmenu.png").convert_alpha(),
                            size=sizes["topmenu"])
        # Positions cards
        self.cards = pygame.sprite.Group()
        self.x = pads["sun"][0] + (pads["menubar"][0] if self.get_preparing() else 0)
        self.starting_x = self.x
        for card in cards:
            image = pygame.image.load(f"assets/cards/card{card.__name__}.png").convert()
            s = Card(self.x, card, image=image, size=sizes["card"])
            self.cards.add(s)
            self.x += sizes["card"][0] + pads["cards"]

        self.shovel = Shovel(sizes["topmenu"][0] + pads["menubar"][0], 0)

    def update(self, screen, sun: int):
        """
        Updates all parts of the interface
        :param screen: Surface
        :param sun: sun count int
        :return: None
        """
        self.frame.update(screen)
        self.cards.update(screen, sun if self.get_preparing() else float("inf"))

        score_digits = list(map(lambda digit: self.digits[digit], str(sun)))
        digit_widths = list(map(lambda image: image.get_width(), score_digits))

        offset = (pads["sun"][0] - sum(digit_widths)) // 2 + (
            pads["menubar"][0] if self.get_preparing() else 0)
        for image, width in zip(score_digits, digit_widths):
            screen.blit(image, (offset, pads["sun"][1]))
            offset += width
        if self.get_preparing() and not self.shovel.taken:
            self.shovel.update(screen)

    def choose_card(self, mouse_pos: tuple, previous_choice: type or Shovel,
                    suns: int) -> type or None:
        """
        Checks mouse position on intersections with cards
        Changes choice or deletes it if clicked the same card
        :param mouse_pos: (x, y)
        :param previous_choice: plant type
        :param suns: int - checks if player can currently afford this plant
        :return: plant type or None
        """
        if self.shovel.can_take(mouse_pos):
            if previous_choice.__class__.__name__ == "Shovel":
                previous_choice.put_back()
                return None
            return self.shovel.take()

        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                choice = card.choose()
                # Last choice deletion
                if choice == previous_choice:
                    return None
                if suns >= choice.sunCost:
                    return choice
        return previous_choice

    def add_card(self, plant: type):
        """
        Adds card during the preparation state
        :param plant: Plant
        :return: None
        """
        if len(self.cards) > 5:
            return
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
        :return: None
        """
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                card.sound.play()
                self.cards.remove(card)
                x = self.starting_x
                for card in self.cards:
                    card.rect.x = x
                    x += sizes["card"][0] + pads["cards"]
                self.x = x
                return

    def move_right(self):
        """
        After removing card all cards need to be moved left
        To remove gap
        :return: None
        """
        dx = pads["menubar"][0]

        self.x += dx
        for card in self.cards:
            card.rect.x += dx
        self.frame.rect.x += dx

    def lock_card(self, plant: type):
        """
        After planting player have to wait until he can use plant again
        :param plant: Plant
        :return: None
        """
        for card in self.cards:
            if card.plant == plant:
                card.set_timer()

    def get_preparing(self) -> bool:
        """
        Check where widget if located
        :return: bool
        """
        return self.frame.rect.x == 100
