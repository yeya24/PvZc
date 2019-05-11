import pygame
from pygame.locals import *

from tiles import *
from plants import *
from other import *

from config import *


class Location:
    """Базовый класс для игровых локаций"""
    parent = None

    def __init__(self, parent):
        self.screen = pygame.display.get_surface()
        # parent для перехода игры между локациями внутри локации
        self.parent = parent

    def event(self, event):
        pass

    def draw(self):
        pass


class StartLocation(Location):
    def __init__(self, parent):
        super().__init__(parent)

    def draw(self):
        ...

    def event(self, event):
        ...


class GameLocation(Location):

    def __init__(self, parent, cards):
        super().__init__(parent)
        # Инициализация игрового интерфейса
        self.plant_choice = None
        self.plant_choice_image = None
        self.suns = starting_sun

        self.suns_group = pygame.sprite.Group()
        # Загрузка заднего фона
        background = pygame.image.load("assets/images/sm_bg.png").convert_alpha()
        self.background = Sprite(0, 0, image=background, size=tuple(sizes["win"].values()))

        # Загрузка меню с индикацией солнышек и выбором цветов
        self.menubar = TopMenu(cards)
        # Создание игрового поля из классов клеток
        self.cells = []
        for y in range(YCells):
            gridRow = []
            for x in range(XCells):
                tile = Grass(x, y)
                gridRow.append(tile)
            self.cells.append(gridRow)

    def draw(self):
        self.background.update(self.screen)
        self.menubar.update(self.screen, self.suns)

        x, y = pygame.mouse.get_pos()

        # Отрисовка клеток справа сверху
        # Ближние к левому краю цветки и их пули проходят по более правым
        for row in self.cells:
            for cell in reversed(row):
                cell.update(self.screen)
                # Изображение тени ратсения на клетку
                if cell.on_top is None and self.plant_choice is not None \
                        and cell.rect.collidepoint((x, y)):
                    self.screen.blit(get_transparent_image(self.plant_choice_image),
                                     (cell.rect.x + (sizes["cell"]["w"] -
                                                     self.plant_choice_image.get_width()) / 2,
                                      cell.rect.y + (sizes["cell"]["h"] -
                                                     self.plant_choice_image.get_height()) / 2))

        # Полупрозрачное изображение выбранного растения
        if self.plant_choice is not None:
            self.screen.blit(self.plant_choice_image,
                             (x - self.plant_choice_image.get_width() / 2,
                              y - self.plant_choice_image.get_height()))

        self.suns_group.update(self.screen)

    def event(self, event):
        if event.type == MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            # Проверка:
            # 1. Что игрок кликнул по падающему солнцу
            # 2. Что игрок выбрал что-либо на верхнем меню
            # 3. Что игрок посадил растение

            # Проверка всех солнц на пересечение с местом клика
            for sun in self.suns_group:
                if sun.rect.collidepoint((x, y)):
                    self.suns += 50
                    sun.kill()
                    return

            # Выбор цветка / лопаты
            if y < sizes["topmenu"]["h"]:
                self.plant_choice = self.menubar.choose_card((x, y), self.plant_choice)
                if self.plant_choice is not None:
                    self.plant_choice_image = plant_images[self.plant_choice.__name__]
                else:
                    self.plant_choice_image = None
            # Быстрый способ выбрать клетку
            else:
                if self.plant_choice is None or self.suns < self.plant_choice.chars["sunCost"]:
                    return

                x -= pads["game"]["x"]
                y -= pads["game"]["y"]
                if x < 0 or y < 0:
                    return

                try:
                    cell = self.cells[y // sizes["cell"]["h"]][x // sizes["cell"]["w"]]
                    if cell.plant(self.plant_choice, self.suns_group):
                        self.suns -= self.plant_choice.chars["sunCost"]
                        self.plant_choice = self.plant_choice_image = None

                except IndexError:
                    return
