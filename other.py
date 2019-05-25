import pygame

from config import *
from sprite import Sprite


def lcm(*args) -> int:
    """
    Returns least common divider
    Needed for updating frames
    :param args: int
    :return:
    """
    import math
    from functools import reduce
    return reduce(lambda a, b: a * b // math.gcd(a, b), map(int, args))


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
            "1": pygame.image.load("misc/1.png").convert_alpha(),
            "2": pygame.image.load("misc/2.png").convert_alpha(),
            "5": pygame.image.load("misc/5.png").convert_alpha(),
            "7": pygame.image.load("misc/7.png").convert_alpha(),
            "0": pygame.image.load("misc/0.png").convert_alpha(),
        }
        # Main frame
        self.frame = Sprite(pos, 0,
                            image=pygame.image.load("misc/topmenu.png").convert_alpha(),
                            size=sizes["topmenu"])
        # Positions cards
        self.cards = pygame.sprite.Group()
        self.x = pads["sun"][0] + (pads["menubar"][0] if pos == 100 else 0)
        self.starting_x = self.x
        for card in cards:
            image = pygame.image.load(f"cards/card{card.__name__}.png").convert()
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
                 image=pygame.image.load(f"cards/card{plant.__name__}.png").convert(),
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


class PlantChoiceMenu:
    def __init__(self, cards):
        self.frame = Sprite(0, sizes["topmenu"][1],
                            image=pygame.image.load(
                                "misc/chooseYourPlants.png").convert_alpha(),
                            size=sizes["choose"])
        self.button_images = list(
            map(lambda image: pygame.transform.smoothscale(image, sizes["letsRock"]), [
                pygame.image.load("misc/letsRock.png").convert_alpha(),
                pygame.image.load("misc/letsRockHighlight.png").convert_alpha()
            ]))
        self.button = Sprite(158, 568, image=self.button_images[0])
        # TODO make several layers support
        self.cards = pygame.sprite.Group()
        self.x = pads["choose"][0]
        for card in cards:
            image = pygame.image.load(f"cards/card{card.__name__}.png").convert()
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


class Card(Sprite):
    """
    Class which keeps plant type
    and card image
    """

    def __init__(self, x: int, plant: type,
                 image: pygame.Surface, size: tuple = None, y: int = 8):
        super().__init__(x, y, image, size)
        self.plant = plant
        # Plant choice sound
        self.sound = pygame.mixer.Sound("audio/seedlift.wav")

    def choose(self) -> type:
        """
        :return: plant choice type
        """
        self.sound.play()
        return self.plant


class Sun(Sprite):
    """
    Sun object which adds sun currency
     if has been clicked on
    """
    speedy = 1.5
    angle = 0

    def __init__(self, x: int, y: int, max_y: int, sunflower: bool = False):
        super().__init__(x, y,
                         image=pygame.image.load("misc/sun.png").convert_alpha(),
                         size=sizes["sun"])

        self.despawn_time = fps * 20
        self.max_y = max_y
        self.speedx = self.up_go = 0
        self.pickup_sound = pygame.mixer.Sound("audio/points.wav")
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


class LawnMover(Sprite):
    """
    Lawn mover class
    Which stay still on the lift side of the field
    and run and kill everything on the line if zombie comes close to the house
    """
    speedX = 3

    def __init__(self, row: int):
        image = pygame.image.load("misc/lawnMover.png").convert_alpha()
        super().__init__(
            pads["game"][0] - image.get_width() / 2,
            pads["game"][1] + sizes["cell"][1] * (row + 1 / 4),
            image=image, size=sizes["lawnmover"]
        )
        self.row = row
        self.running = False
        self.sound = pygame.mixer.Sound("audio/lawnmower.wav")

    def update(self, screen) -> bool:
        """
        Changes position if running
        Returns True if is out of window bounds
        :param screen: pygame.display
        :return : bool
        """
        if self.running:
            if self.rect.x > sizes["win"][0]:
                return True

            self.rect.x += self.speedX
        self._draw(screen)
        return False

    def run(self):
        self.sound.play()
        self.running = True


class StageIndicator(Sprite):
    pass


class MenuButton(Sprite):
    pass
