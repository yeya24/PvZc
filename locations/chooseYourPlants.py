import pygame
from pygame.locals import *

from config import sizes, starting_sun
from interface import PlantChoiceMenu, TopMenu
from sprites import Sprite
from .gameLocation import GameLocation
from .location import Location


class LevelPreparationLocation(Location):
    def __init__(self, parent):
        super().__init__(parent)
        # Location music
        pygame.mixer_music.load("assets/audio/chooseYourSeeds.mp3")
        pygame.mixer_music.play(loops=-1)

        self.bg = Sprite(0, 0,
                         image=pygame.image.load("assets/misc/bg.png").convert())
        # At the begging camera moves to the right side of background
        self.move_times = (self.bg.image.get_width() - sizes["win"][0]) / 5
        from plants import PeaShooter, Sunflower, PotatoMine, WallNut, SnowPea, Chomper, CherryBomb, Repeater
        # Card choices
        self.plant_choice_widget = PlantChoiceMenu(
            [PotatoMine, Sunflower, SnowPea, CherryBomb, Chomper, Repeater, WallNut, PeaShooter])
        # Menu which usually displays suns and chosen cards
        # New cards added here
        self.top_menu = TopMenu(pos=0)
        # Sounds and images for pre-game state
        self.ready_set_plant = pygame.mixer.Sound("assets/audio/readysetplant.wav")
        self.ready_set_plant_images = [
            pygame.image.load("assets/misc/StartReady.png").convert_alpha(),
            pygame.image.load("assets/misc/StartSet.png").convert_alpha(),
            pygame.image.load("assets/misc/StartPlant.png").convert_alpha(),
        ]
        self.counter = 0

    def update(self):
        if self.move_times > 0:  # Moves right before seeds choice
            self.bg.rect.x -= 5
            self.move_times -= 1
        elif self.move_times < 0:  # Moves left after seeds choice
            self.bg.rect.x += 5
            self.move_times += 1
            if self.move_times == 0:
                self.ready_set_plant.play()
                self.counter = 1

        self.bg.update(self.screen)
        if not self.move_times and not self.counter:
            self.plant_choice_widget.update(self.screen, pygame.mouse.get_pos())
            self.top_menu.update(self.screen, starting_sun)
        elif self.counter:
            self.counter += 1
            image = None
            if self.counter >= 100:  # Change game location on game
                data = object  # Level data
                self.top_menu.move_right()
                self.parent.change_location(
                    GameLocation(self, data, self.top_menu))
            # Ready Set Plant messages
            elif self.counter >= 80:
                image = self.ready_set_plant_images[2]
            elif self.counter >= 40:
                image = self.ready_set_plant_images[1]
            elif self.counter >= 5:
                image = self.ready_set_plant_images[0]

            if image is not None:
                self.screen.blit(image,
                                 ((sizes["win"][0] - image.get_width()) / 2,
                                  (sizes["win"][1] - image.get_height()) / 2))

    def event(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            self.top_menu.remove_card(mouse_pos)
            choice = self.plant_choice_widget.choose_card(mouse_pos)
            if choice is not None:
                self.top_menu.add_card(choice)

            if self.plant_choice_widget.button_click(mouse_pos):
                self.move_times = -(self.bg.image.get_width() - sizes["win"][0] - 220) / 5
