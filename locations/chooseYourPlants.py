import pygame
from pygame.locals import *

from config import sizes, starting_sun
from interface import PlantChoiceMenu, TopMenu
from sprites import Sprite
from .location import Location
from .gameLocation import GameLocation


class LevelPreparationLocation(Location):
    def __init__(self, parent):
        super().__init__(parent)
        pygame.mixer_music.load("assets/audio/chooseYourSeeds.mp3")
        pygame.mixer_music.play(loops=-1)

        self.bg = Sprite(0, 0,
                         image=pygame.image.load("assets/misc/bg.png").convert())
        self.move_right_times = (self.bg.image.get_width() - sizes["win"][0]) / 5
        from plants import PeaShooter, Sunflower, SnowPea
        self.plant_choice_widget = PlantChoiceMenu([PeaShooter, Sunflower, SnowPea])
        self.top_menu = TopMenu(pos=0)

    def update(self):
        if self.move_right_times:
            self.bg.rect.x -= 5
            self.move_right_times -= 1

        self.bg.update(self.screen)
        if not self.move_right_times:
            self.plant_choice_widget.update(self.screen, pygame.mouse.get_pos())
            self.top_menu.update(self.screen, starting_sun)

        # TODo Выбор уровня
        data = object  # Данные уровня
        from plants import PeaShooter, Sunflower, WallNut, PotatoMine, SnowPea, Repeater
        self.top_menu.move_right()
        self.parent.change_location(
            GameLocation(self, data, self.top_menu))
        pass

    def event(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            self.top_menu.remove_card(mouse_pos)
            choice = self.plant_choice_widget.choose_card(mouse_pos)
            if choice is not None:
                self.top_menu.add_card(choice)
