from .tile import Tile


class Grass(Tile):
    def __init__(self, col, row):
        super().__init__(col, row, True)
