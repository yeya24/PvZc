import itertools

import pygame
from pygame.locals import *


def greyscale(img: pygame.Surface) -> pygame.Surface:
    """
    Makes image gray using 0.298, 0.587, 0.114 formula
    :param img: Surface
    :return: Surface
    """
    arr = pygame.surfarray.array3d(img)
    arr = arr.dot([0.298, 0.587, 0.114])[:, :, None].repeat(3, axis=2)
    return pygame.surfarray.make_surface(arr)


def lcm(*args: int) -> int:
    """
    Returns least common divider
    Needed for updating frames
    :param args: int
    :return: lcm of [*args]
    """
    import math
    from functools import reduce
    return reduce(lambda a, b: a * b // math.gcd(a, b), map(int, args))


def transform_image(image: pygame.Surface,
                    r: int = 255, g: int = 255, b: int = 255,
                    alpha: int = 128, special_flag: int = BLEND_RGBA_MULT) -> pygame.Surface:
    """
    Function for transforming images
    By default makes the lighter
    Used not to copy same code with copying and filling image
    :param image: Surface
    :param r: R component
    :param g: G component
    :param b: B component
    :param alpha: A component
    :param special_flag: BLEND_RGBA_... (MULT, ADD)
    :return: Surface
    """
    im = image.copy().convert_alpha()
    im.fill((r, g, b, alpha), None, special_flag)
    return im


def get_images_from_sprite_sheet(filename: str,
                                 rows: int, cols: int,
                                 size: tuple = None, ratio: float = None,
                                 cycle: bool = True) -> itertools.cycle or list:
    """
    Converts image into list or cycle of images from given sprite sheet
    :param filename: path
    :param rows: int - rows count in sprite sheet
    :param cols: int - cols count in sprite sheet
    :param size: (w, h) - wanted size of images
    :param ratio: float - multiply width or height by ratio
    :param cycle: bool - return itertools.cycle or list
    :return: itertools.cycle or [Surface]
    """
    rects = []

    sheetImage = pygame.image.load(filename).convert_alpha()
    spriteWidth = sheetImage.get_width() // cols
    spriteHeight = sheetImage.get_height() // rows

    for y in range(0, sheetImage.get_height(), spriteHeight):
        if y + spriteHeight > sheetImage.get_height():
            continue
        for x in range(0, sheetImage.get_width(), spriteWidth):
            if x + spriteWidth > sheetImage.get_width():
                continue

            rects.append((x, y, spriteWidth, spriteHeight))

    returnedSurfaces = []
    for rect in rects:
        surf = pygame.Surface((rect[2], rect[3]), 0, sheetImage)
        surf.blit(sheetImage, (0, 0), rect, pygame.BLEND_RGBA_ADD)

        if size:
            surf = pygame.transform.smoothscale(surf, size)
        elif ratio:
            surf = pygame.transform.smoothscale(surf,
                                                (int(spriteWidth * ratio),
                                                 int(spriteHeight * ratio)))
        returnedSurfaces.append(surf)
    size = size or (spriteWidth, spriteHeight)
    if cycle:
        returnedSurfaces = itertools.cycle(returnedSurfaces)
    return returnedSurfaces, size
