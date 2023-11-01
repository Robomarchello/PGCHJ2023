import pygame
from json import load


class Level:
    def __init__(self, path, ScreenSize, tileSize):
        self.screenRect = pygame.Rect((0, 0), ScreenSize)
        with open(path) as file:
            self.tiles = load(file)['level']

        self.tileSize = tileSize
        self.tileRects = []

        self.vents = False

    def draw(self, screen, offset):
        self.screenRect.topleft = -offset
        self.tileRects = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * self.tileSize, y * self.tileSize,
                    self.tileSize, self.tileSize
                )
                display_rect = rect.copy()
                display_rect.x += offset[0]
                display_rect.y += offset[1]

                if not self.screenRect.colliderect(rect):
                    continue

                if tile == 1:
                    pygame.draw.rect(screen, (105, 105, 105), display_rect)
                    self.tileRects.append(rect)

                if tile == 2:
                    pygame.draw.rect(screen, (150, 150, 150), display_rect)

                pygame.draw.rect(screen, (0, 0, 0), display_rect, width=1)