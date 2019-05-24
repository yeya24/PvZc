import sys

import pygame
from pygame.locals import *

from config import fps, sizes
from locations import MainMenuLocation


class Game:
    def __init__(self, location):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode(sizes["win"])
        pygame.display.set_caption("PvZ α")

        self.location = location(self)

    def event(self, event):
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP and event.key == K_ESCAPE:
            ...

        pygame.display.update()

    def draw(self):
        self.location.update()
        pygame.display.flip()
        for event in pygame.event.get():
            self.location.event(event)
            self.event(event)

    def change_location(self, location):
        # Смена должна просиходить как минимум после 1 обновления локации
        self.location = location


def main():
    game = Game(MainMenuLocation)
    clock = pygame.time.Clock()

    while True:
        clock.tick(fps)
        game.draw()


if __name__ == "__main__":
    main()
