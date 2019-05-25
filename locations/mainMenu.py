from .chooseYourPlants import LevelPreparationLocation
from .location import Location


class MainMenuLocation(Location):
    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        self.parent.change_location(LevelPreparationLocation(self.parent))

    def event(self, event):
        ...
