import pygame
from pygame.locals import *

from locations import GameLocation  # StartLocation
from plants import PeaShooter, Sunflower  # delete

import sys

from config import fps, sizes


class Game:
    def __init__(self, location):
        pygame.init()
        pygame.display.set_mode(sizes["win"])
        pygame.display.set_caption("PvZ α")

        self.location = location(self, [PeaShooter, Sunflower])

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


"""
PvZ
├──Game
|  . 
├──Location
|  ├──StartLocation
|  |
|  ├──GameLocation
|  |
|  ├──LevelPreparationLocation
|  |
|  ├──MoveLocation
|  |
|  ├──MenuLocation
|  .
├──Sprite
|  ├──Tile
|  |  ├──Grass
|  |  .
|  ├──Plant
|  |  ├──Peashooter
|  |  |
|  |  ├──Sunflower
|  |  |
|  |  ├──PotatoMine
|  |  |
|  |  ├──WallNut
|  |  |
|  |  ├──CherryBomb
|  |  |
|  |  ├──Repeater
|  |  |
|  |  ├──SnowPea
|  |  |
|  |  ├──Chomper
|  |  .
|  ├──Projectile
|  |  ├──PeashooterProjectile
|  |  |
|  |  ├──FrozenProjectile
|  |  .
|  ├──Zombie
|  |  ├──NormalZombie
|  |  |
|  |  ├──FlagZombie
|  |  |
|  |  ├──ConeHeadZombie
|  |  |
|  |  ├──PoleVaultingZombie
|  |  |
|  |  ├──BucketHeadZombie
|  |  .
|  ├──TopMenu
|  |  .
|  ├──Cards
|  |  .
|  ├──Sun
|  |  .
|  ├──
|  |
.


Game--Location--Tile--Plant--Projectile
"""

if __name__ == "__main__":
    main()
