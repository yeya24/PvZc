import pygame
from pygame.locals import *

from sprite import Sprite
from tiles import Grass
from plants import plant_images
from other import Sun, TopMenu, get_transparent_image
from zombies import NormalZombie, ConeHeadZombie, PoleVaultingZombie, BucketHeadZombie, FlagZombie

from config import *

import random


class Location:
    """Базовый класс для игровых локаций"""
    parent = None

    def __init__(self, parent):
        self.screen = pygame.display.get_surface()
        # parent для перехода игры между локациями внутри локации
        self.parent = parent

    def event(self, event):
        pass

    def update(self):
        pass


class StartLocation(Location):
    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        ...

    def event(self, event):
        ...


class GameLocation(Location):
    def __init__(self, parent, cards):
        super().__init__(parent)
        # Инициализация игрового интерфейса
        self.plant_choice = self.plant_choice_image = None
        self.suns = starting_sun
        # Группы спрайтов солнц и зомби, т. к. порядок их отображения не важен
        self.suns_group = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        # Загрузка заднего фона
        self.background = Sprite(0, 0,
                                 image=pygame.image.load("assets/images/sm_bg.png").convert_alpha(),
                                 size=tuple(sizes["win"].values()))

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

        # Вызов падающего солнца каждые sun_drop_delay секунд
        pygame.time.set_timer(USEREVENT + 1, sun_drop_delay * 1000)

        self.zombies.add(NormalZombie(3))

    def update(self):
        self.background.update(self.screen)
        self.menubar.update(self.screen, self.suns)
        self.zombies.update(self.screen)

        x, y = pygame.mouse.get_pos()
        # Отрисовка клеток справа сверху
        # Ближние к левому краю цветки и их пули проходят по более правым
        for row in self.cells:
            for cell in reversed(row):
                cell.update(self.screen)
                # Изображение тени растения на клетку
                if cell.on_top is None and self.plant_choice is not None \
                        and cell.rect.collidepoint((x, y)):
                    # Располагается в середине
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
        if event.type == USEREVENT + 1:
            self.drop_sun()

        elif event.type == MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            # Проверка:
            # 1. Что игрок кликнул по падающему солнцу
            # 2. Что игрок выбрал что-либо на верхнем меню
            # 3. Что игрок посадил растение

            # Проверка всех солнц на пересечение с местом клика
            for sun in self.suns_group:
                if sun.rect.collidepoint((x, y)):
                    self.suns += 25
                    sun.kill()
                    return

            # Выбор цветка / лопаты
            if y < sizes["topmenu"]["h"]:
                self.plant_choice = self.menubar.choose_card((x, y), self.plant_choice)
                self.plant_choice_image = None
                if self.plant_choice is not None:
                    self.plant_choice_image = plant_images[self.plant_choice.__name__]
            else:
                # Быстрый способ выбрать клетку
                # Если текущее количество солнц меньше стоимости выбранного растения
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

    def drop_sun(self):
        max_y = random.randint(sizes["win"]["h"] // 3, sizes["win"]["h"] * 2 // 3)
        x = random.randint(sizes["win"]["w"] // 10, sizes["win"]["w"] * 9 // 10)
        self.suns_group.add(Sun(x, sizes["topmenu"]["h"], max_y))


class LevelPreparationLocation(Location):
    pass
