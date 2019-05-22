import random

import pygame
from pygame.locals import *

from sprite import Sprite
from animation import transform_image
from config import *
from other import Sun, TopMenu
from tiles import Grass
from zombies import NormalZombie


class Location:
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
        self.suns = 2500  # starting_sun
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
            grid_row = []
            for x in range(XCells):
                tile = Grass(x, y)
                grid_row.append(tile)
            self.cells.append(grid_row)

        # Вызов падающего солнца каждые sun_drop_delay секунд
        pygame.time.set_timer(USEREVENT + 1, sun_drop_delay * 1000)
        # Музыка
        pygame.mixer_music.load("assets/audio/grasswalk.mp3")
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer_music.play(loops=-1)

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
                if cell.isempty() and self.plant_choice is not None \
                        and cell.rect.collidepoint((x, y)):
                    # Располагается в середине клетки
                    self.screen.blit(transform_image(self.plant_choice_image),
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
                             key=lambda zombie: zombie.row * XCells + zombie.col):
            zombie.update(self.screen)

        self.game_event()
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
                if sun.check_collision((x, y)):
                    self.suns += 25
                    return

            # Выбор цветка / лопаты
            if y < sizes["topmenu"][1]:
                self.plant_choice = self.menubar.choose_card((x, y), self.plant_choice)
                self.plant_choice_image = None
                if self.plant_choice is not None:
                    self.plant_choice_image = self.plant_choice.shadow.convert_alpha()
            else:
                # Быстрый способ выбрать клетку
                # Если текущее количество солнц меньше стоимости выбранного растения
                if self.plant_choice is None or self.suns < self.plant_choice.sunCost:
                    return

                x -= pads["game"][0]
                y -= pads["game"][1]
                if x < 0 or y < 0:
                    return
                try:
                    cell = self.cells[y // sizes["cell"][1]][x // sizes["cell"][0]]
                    if cell.plant(self.plant_choice, self.suns_group, self.projectiles):
                        self.suns -= self.plant_choice.sunCost
                        self.plant_choice = self.plant_choice_image = None
                except IndexError:
                    return

    def drop_sun(self):
        max_y = random.randint(sizes["win"][1] // 3, sizes["win"][1] * 2 // 3)
        x = random.randint(sizes["win"][0] // 10, sizes["win"][0] * 9 // 10)
        self.suns_group.add(Sun(x, sizes["topmenu"][1], max_y))

    def game_event(self):
        # TODO оптимизировать все проверки
        # Проверка пуль на столкновение
        for projectile in self.projectiles:
            for zombie in self.zombies:
                if projectile.row == zombie.row and projectile.rect.x >= zombie.rect.x:
                    zombie.take_damage(projectile)
                    # Играть звук попадания
                    break

        # Проврека пересечений между зомби и растениями
        # Если находятся в одной клетке, заставить зомби есть растение
        for zombie in filter(lambda zombie: not zombie.busy(), self.zombies):
            for cell in filter(lambda cell: not cell.isempty() and cell.col == zombie.col,
                               self.cells[zombie.row]):
                plant = cell.planted
                zombie.change_target(plant)

        # Взрыв картофельной мины
        for zombie in self.zombies:
            for cell in filter(lambda cell: not cell.isempty() and cell.col == zombie.col,
                               self.cells[zombie.row]):
                plant = cell.planted.sprite
                if plant.__class__.__name__ == "PotatoMine":
                    if plant.armed:
                        plant.explode(zombie)

        # TODO проигрыш


class LevelPreparationLocation(Location):
    pass
