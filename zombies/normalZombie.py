from misc import get_images_from_sprite_sheet
from .zombie import Zombie


class NormalZombie(Zombie):
    def __init__(self, row: int):
        images, size = get_images_from_sprite_sheet("assets/zombies/normalZombie.png",
                                                    10, 5, ratio=4 / 5)
        super().__init__(row, images, size)
