import random

import pygame
from pygame.locals import *

from config import pads, sizes, sun_drop_delay, XCells, YCells, starting_sun
from misc import transform_image
from sprites import LawnMower, Sprite, Sun
from tiles import Grass
from zombies import *
from .location import Location


class GameLocation(Location):
    def __init__(self, parent, level, top_menu):
        super().__init__(parent)
        # Инициализация игрового интерфейса
        self.plant_choice = self.plant_choice_image = None
        self.suns = starting_sun  # starting_sun
        # Группы спрайтов солнц и зомби, т. к. порядок их отображения не важен
        self.suns_group = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.lawnmovers = [LawnMower(row) for row in range(5)]

        # Загрузка заднего фона
        self.background = Sprite(0, 0,
                                 image=pygame.image.load("assets/misc/sm_bg.png").convert_alpha(),
                                 size=sizes["win"])
        # Загрузка меню с индикацией солнышек и выбором цветов
        self.menubar = top_menu
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
        self.zombies.add(BucketHeadZombie(1))

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
        self.lawnmovers_update()
        # Полупрозрачное изображение выбранного растения
        if self.plant_choice is not None:
            self.screen.blit(self.plant_choice_image,
                             (x - self.plant_choice_image.get_width() / 2,
                              y - self.plant_choice_image.get_height()))
        # Сначала отрисовываются верхние правые
        for zombie in sorted(self.zombies.sprites(),
                             key=lambda zombie: zombie.row * XCells + zombie.col):
            zombie.update(self.screen)
        self.zombie_targeting()
        self.projectiles.update(self.screen)
        self.projectile_collisions_check()
        self.suns_group.update(self.screen)

    def event(self, event):
        """
        Responds to game events
        :param event: pygame.event
        :return: None
        """
        if event.type == USEREVENT + 1:
            self.drop_sun()

        elif event.type == MOUSEBUTTONUP and event.button == 1:
            x, y = pygame.mouse.get_pos()
            print((x, y))
            # Проверка:
            # 1. Что игрок кликнул по падающему солнцу
            # 2. Что игрок выбрал что-либо на верхнем меню
            # 3. Что игрок посадил растение

            # Проверка всех солнц на пересечение с местом клика
            for sun in self.suns_group:
                if sun.check_collision((x, y)):
                    sun.fly()
                    self.suns += 25
                    return

            # Выбор цветка / лопаты
            self.plant_choice = self.menubar.choose_card((x, y), self.plant_choice)
            self.plant_choice_image = None
            if self.plant_choice is not None:
                self.plant_choice_image = self.plant_choice.shadow.convert_alpha()

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
                    self.menubar.lock_card(self.plant_choice)
                    self.suns -= self.plant_choice.sunCost
                    self.plant_choice = self.plant_choice_image = None
            except IndexError:
                return

    def drop_sun(self):
        """
        This method is called periodically through custom pygame event
        Drops sun in random place on random height
        """
        max_y = random.randint(sizes["win"][1] // 3, sizes["win"][1] * 2 // 3)
        x = random.randint(sizes["win"][0] // 10, sizes["win"][0] * 9 // 10)
        self.suns_group.add(Sun(x, sizes["topmenu"][1], max_y))

    def projectile_collisions_check(self):
        """
        Checks all projectiles on collisions with zombies
        Calls zombie method take_damage if so
        """
        for zombie in self.zombies:
            # Checks for hits
            for projectile in filter(lambda projectile:
                                     projectile.row == zombie.row and
                                     projectile.rect.x >= zombie.rect.x,
                                     self.projectiles):
                zombie.take_damage(projectile)

            # Checks for potato mine explosions
            for cell in filter(lambda cell: cell.col == zombie.col,
                               self.cells[zombie.row]):
                plant = cell.planted.sprite
                if plant.__class__.__name__ == "PotatoMine":
                    if plant.armed:
                        plant.explode(zombie)

            # Check if chompers can eat zombie
            for cell in self.cells[zombie.row][zombie.col - 1: zombie.col + 1]:
                plant = cell.planted.sprite
                if plant.__class__.__name__ == "Chomper":
                    if not plant.busy():
                        plant.catch(zombie)

        # Check for cherryBomb explosion
        for row in self.cells:
            for cell in row:
                plant = cell.planted.sprite
                if plant.__class__.__name__ == "CherryBomb":
                    if plant.armed and plant.health > 0:
                        row, col = plant.coords
                        plant.explode(*filter(
                            lambda zombie: zombie.row in [row - 1, row, row + 1] and
                                           zombie.col in [col - 1, col, col + 1], self.zombies)
                                      )

    def lawnmovers_update(self):
        """
        Checks for zombie crossing the last cell
        If row lawnmover exists, make it run
        Else game is lost
        """

        # Проверка что зомби зашел за границу клеток
        # - запуск загонокосилки / проигрыш
        for zombie in self.zombies:
            if zombie.col < 0:
                landmover = self.lawnmovers[zombie.row]
                if landmover is None:
                    self.lose()
                    return
                landmover.run()

        for ind, landmover in enumerate(self.lawnmovers):
            if landmover is None:
                continue
            if landmover.update(self.screen):
                self.lawnmovers[ind] = None
                continue

            for zombie in self.zombies:
                if landmover.running and zombie.row == landmover.row and \
                        landmover.rect.x > zombie.rect.x:
                    zombie.kill()

    def zombie_targeting(self):
        """
        Checks for cell intersections between plants and zombies
        Makes zombie eat plant if so
        """
        for zombie in filter(lambda zombie: not zombie.busy(), self.zombies):
            for cell in filter(lambda cell: not cell.isempty() and cell.col == zombie.col,
                               self.cells[zombie.row]):
                plant = cell.planted
                zombie.change_target(plant)

    def lose(self):
        pass
        # Game over / main menu
