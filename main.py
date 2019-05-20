import sys

import pygame
from pygame.locals import *

from config import fps, sizes
from locations import GameLocation  # StartLocation
from plants import PeaShooter, PotatoMine, SnowPea, Sunflower, WallNut  # delete


class Game:
    def __init__(self, location):
        pygame.init()
        pygame.display.set_mode(sizes["win"])
        pygame.display.set_caption("PvZ α")

        self.location = location(self, [PeaShooter, Sunflower, WallNut, PotatoMine, SnowPea])

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


def main():
    game = Game(GameLocation)
    clock = pygame.time.Clock()

    while True:
        clock.tick(fps)
        game.draw()


if __name__ == "__main__":
    main()
