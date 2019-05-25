from misc import get_images_from_sprite_sheet
from .zombie import Zombie


class BucketHeadZombie(Zombie):
    health = 1300

    def __init__(self, row: int):
        images, size = get_images_from_sprite_sheet("assets/zombies/bucketHeadZombie.png",
                                                    10, 5, ratio=4 / 5)
        super().__init__(row, images, size)
