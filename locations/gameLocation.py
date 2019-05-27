import random

import pygame
from pygame.locals import *

from config import pads, sizes, starting_sun, sun_drop_delay, XCells, YCells
from misc import transform_image
from sprites import LawnMower, Sprite, Sun
from tiles import Grass
from zombies import *
from .location import Location


class GameLocation(Location):
    def __init__(self, parent, level, top_menu):
        super().__init__(parent)
        # Game interface
        self.plant_choice = self.plant_choice_image = None
        self.suns = starting_sun + 2000  # starting_sun
        # Sprite groups for different game objects
        self.suns_group = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.lawnmovers = [LawnMower(row) for row in range(5)]

        # Background is a sprite for easier drawing
        self.background = Sprite(0, 0,
                                 image=pygame.image.load("assets/misc/sm_bg.png").convert_alpha(),
                                 size=sizes["win"])
        # Menu with plant choices, shovel and suns count indication
        self.menubar = top_menu
        # Creating game field
        self.cells = []
        for y in range(YCells):
            grid_row = []
            for x in range(XCells):
                tile = Grass(x, y)
                grid_row.append(tile)
            self.cells.append(grid_row)

        # Adds event of falling sun for every sun_drop_delay seconds
        pygame.time.set_timer(USEREVENT + 1, sun_drop_delay * 1000)
        # Music
        pygame.mixer_music.load("assets/audio/grasswalk.mp3")
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer_music.play(loops=-1)

        self.zombies.add(NormalZombie(0))
        self.zombies.add(BucketHeadZombie(1))

    def update(self):
        self.background.update(self.screen)
        self.menubar.update(self.screen, self.suns)

        x, y = pygame.mouse.get_pos()
        # Draws from right to left
        for row in self.cells:
            for cell in reversed(row):
                cell.update(self.screen)
                # Transparent image of chosen plant
                if cell.isempty() and self.plant_choice is not None \
                        and cell.rect.collidepoint((x, y)) and \
                        self.plant_choice.__class__.__name__ != "Shovel":
                    # In the middle of the cell
                    self.screen.blit(transform_image(self.plant_choice_image),
                                     cell.get_middle_pos(self.plant_choice_image))
        self.lawnmovers_update()
        # Start drawing from right top
        for zombie in sorted(self.zombies.sprites(),
                             key=lambda z: z.row * XCells + z.col):
            zombie.update(self.screen)
        self.zombie_targeting()
        # Draw choice near the mouse
        if self.plant_choice is not None:
            self.screen.blit(self.plant_choice_image,
                             (x - self.plant_choice_image.get_width() / 2,
                              y - self.plant_choice_image.get_height()))

        self.projectiles.update(self.screen)
        self.projectile_collisions_check()
        self.suns_group.update(self.screen)

    def event(self, event):
        """
        Responds to game events
        :param event: pygame.event
        :return: None
        """
        # Drop sun
        if event.type == USEREVENT + 1:
            self.drop_sun()

        elif event.type == MOUSEBUTTONUP and event.button == 1:
            x, y = pygame.mouse.get_pos()
            # Check order:
            # 1. Player clicked on a sun
            # 2. Player has chosen anything on the top menu
            # 3. Player planted plant / removed one using shovel

            # Suns check
            for sun in self.suns_group:
                if sun.check_collision((x, y)):
                    sun.fly()
                    self.suns += 25
                    return

            # Top menu choice check
            choice = self.menubar.choose_card((x, y), self.plant_choice, self.suns)
            if choice != self.plant_choice:
                self.plant_choice = choice
                self.plant_choice_image = None
                if self.plant_choice is not None:
                    self.plant_choice_image = self.plant_choice.get_shadow()
                    return

            # Plant / use shovel
            # If player's suns count is lesser than the needed for this plant
            if self.plant_choice.__class__.__name__ != "Shovel":
                if self.plant_choice is None or self.suns < self.plant_choice.sunCost:
                    return

            x -= pads["game"][0]
            y -= pads["game"][1]
            if x < 0 or y < 0:
                self.plant_choice = self.plant_choice_image = None
                return
            try:
                cell = self.cells[y // sizes["cell"][1]][x // sizes["cell"][0]]
                if self.plant_choice.__class__.__name__ == "Shovel":
                    # If player is using shovel remove plant
                    if cell.remove_plant():
                        self.plant_choice.put_back()
                        self.plant_choice = self.plant_choice_image = None
                elif cell.plant(self.plant_choice, self.suns_group, self.projectiles):
                    # Else plant
                    self.menubar.lock_card(self.plant_choice)
                    self.suns -= self.plant_choice.sunCost
                    self.plant_choice = self.plant_choice_image = None
            except IndexError:
                self.plant_choice = self.plant_choice_image = None

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
            for projectile in filter(lambda p:
                                     p.row == zombie.row and
                                     p.rect.x >= zombie.rect.x,
                                     self.projectiles):
                zombie.take_damage(projectile)

            # Checks for potato mine explosions
            for cell in filter(lambda c: c.col == zombie.col,
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
                            lambda z: z.row in [row - 1, row, row + 1] and
                                      z.col in [col - 1, col, col + 1], self.zombies)
                                      )

    def lawnmovers_update(self):
        """
        Checks for zombie crossing the last cell
        If row lawnmover exists, make it run
        Else game is lost
        """

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
        for zombie in filter(lambda z: not z.busy(), self.zombies):
            for cell in filter(lambda c: not c.isempty() and c.col == zombie.col,
                               self.cells[zombie.row]):
                plant = cell.planted
                zombie.change_target(plant)

    def lose(self):
        pass
        # Game over / main menu
