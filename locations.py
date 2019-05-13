import pygame
from pygame.locals import *

from sprite import Sprite
from tiles import Grass
from plants import plant_images
from other import Sun, TopMenu
from zombies import NormalZombie, ConeHeadZombie, PoleVaultingZombie, BucketHeadZombie, FlagZombie
from animation import get_transparent_image

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
        self.suns = 100
        # Группы спрайтов солнц и зомби, т. к. порядок их отображения не важен
        self.suns_group = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        # Загрузка заднего фона
        self.background = Sprite(0, 0,
                                 image=pygame.image.load("assets/images/sm_bg.png").convert_alpha(),
                                 size=sizes["win"])

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

        self.zombies.add(BucketHeadZombie(2))
        self.zombies.add(ConeHeadZombie(1))
        self.zombies.add(NormalZombie(0))

    def update(self):
        self.background.update(self.screen)
        self.menubar.update(self.screen, self.suns)

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
                                     (cell.rect.x + (sizes["cell"][0] -
                                                     self.plant_choice_image.get_width()) / 2,
                                      cell.rect.y + (sizes["cell"][1] -
                                                     self.plant_choice_image.get_height()) / 2))

        # Полупрозрачное изображение выбранного растения
        if self.plant_choice is not None:
            self.screen.blit(self.plant_choice_image,
                             (x - self.plant_choice_image.get_width() / 2,
                              y - self.plant_choice_image.get_height()))
        # Сначала отрисовываются верхние правые
        for zombie in sorted(self.zombies.sprites(),
                             key=lambda zombie: zombie.row * XCells + zombie.cell):
            zombie.update(self.screen)

        self.projectile_collision_check()
        self.projectiles.update(self.screen)
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
            if y < sizes["topmenu"][1]:
                self.plant_choice = self.menubar.choose_card((x, y), self.plant_choice)
                self.plant_choice_image = None
                if self.plant_choice is not None:
                    self.plant_choice_image = plant_images[self.plant_choice.__name__]
            else:
                # Быстрый способ выбрать клетку
                # Если текущее количество солнц меньше стоимости выбранного растения
                if self.plant_choice is None or self.suns < self.plant_choice.chars["sunCost"]:
                    return

                x -= pads["game"][0]
                y -= pads["game"][1]
                if x < 0 or y < 0:
                    return

                try:
                    cell = self.cells[y // sizes["cell"][1]][x // sizes["cell"][0]]
                    if cell.plant(self.plant_choice, self.suns_group, self.projectiles):
                        self.suns -= self.plant_choice.chars["sunCost"]
                        self.plant_choice = self.plant_choice_image = None

                except IndexError:
                    return

    def drop_sun(self):
        max_y = random.randint(sizes["win"][1] // 3, sizes["win"][1] * 2 // 3)
        x = random.randint(sizes["win"][0] // 10, sizes["win"][0] * 9 // 10)
        self.suns_group.add(Sun(x, sizes["topmenu"][1], max_y))

    def projectile_collision_check(self):
        for projectile in self.projectiles.sprites():
            for zombie in self.zombies.sprites():
                if projectile.row == zombie.row and projectile.rect.x >= zombie.rect.x:
                    zombie.take_damage(projectile)
                    # Играть звук попадания
                    break


class LevelPreparationLocation(Location):
    pass
