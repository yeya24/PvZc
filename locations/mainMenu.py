import pygame
from pygame.locals import *

from config import sizes
from sprite import Sprite
from .location import Location
from interface import Button
import sys


class MainMenuLocation(Location):
    def __init__(self, parent):
        super().__init__(parent)
        self.bg = Sprite(0, 0,
                         image=pygame.image.load("assets/misc/mainMenu.png").convert(),
                         size=sizes["win"])
        pygame.mixer.music.load("assets/audio/intro.mp3")
        pygame.mixer.music.play(-1)
        self.play_button = Button(430, 65,
                                  pygame.image.load(
                                      "assets/misc/start.png").convert_alpha(),
                                  pygame.image.load(
                                      "assets/misc/startHighlight.png").convert_alpha())
        self.exit = Button(748, 535,
                           pygame.image.load("assets/misc/potQuit.png").convert(),
                           pygame.image.load("assets/misc/potQuitHighlight.png").convert())

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        self.bg.update(self.screen)
        self.play_button.update(self.screen, mouse_pos)
        self.exit.update(self.screen, mouse_pos)
        #
        pass

    def event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if self.play_button.click(mouse_pos):
                from .chooseYourPlants import LevelPreparationLocation
                self.parent.change_location(LevelPreparationLocation(self.parent))
            if self.exit.click(mouse_pos):
                sys.exit()

