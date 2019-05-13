import itertools

import pygame
from pygame.locals import *


def get_transparent_image(image, density=255, alpha=128, special_flag=BLEND_RGBA_MULT):
    im = image.copy()
    im.fill((density, density, density, alpha), None, special_flag)
    return im


def getImagesFromSpriteSheet(filename, rows, cols, size=None, ratio=None):
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

    return itertools.cycle(returnedSurfaces), (spriteWidth, spriteHeight)
