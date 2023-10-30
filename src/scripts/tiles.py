import pygame
from json import load


class Level:
    def __init__(self, path, ScreenSize, tileSize):
        self.screenRect = pygame.Rect((0, 0), ScreenSize)
        with open(path) as file:
            self.tiles = load(file)['level']

        self.tileSize = tileSize

    def draw(self, screen, offset):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * self.tileSize + offset[0], y * self.tileSize + offset[1],
                    self.tileSize, self.tileSize
                )

                if not self.screenRect.colliderect(rect):
                    continue

                if tile == 1:
                    pygame.draw.rect(screen, (105, 105, 105), rect)

                pygame.draw.rect(screen, (0, 0, 0), rect, width=1)