import pygame


class _Location:
    parent = None

    def __init__(self, parent):
        self.screen = pygame.display.get_surface()
        # parent is needed for changing locations within locations
        self.parent = parent

    def event(self, event):
        pass

    def update(self):
        pass
