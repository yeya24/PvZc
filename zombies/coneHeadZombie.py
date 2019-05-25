from misc import get_images_from_sprite_sheet
from .zombie import Zombie


class ConeHeadZombie(Zombie):
    health = 560

    def __init__(self, row: int):
        images, size = get_images_from_sprite_sheet("assets/zombies/coneHeadZombie.png",
                                                    10, 5, ratio=4 / 5)
        super().__init__(row, images, size)
