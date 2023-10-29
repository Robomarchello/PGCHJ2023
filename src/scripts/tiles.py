import pygame
from json import load


class Level:
    def __init__(self, path, tileSize):
        with open(path) as file:
            self.tiles = load(file)['level']

        self.tileSize = tileSize

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * self.tileSize, y * self.tileSize,
                    self.tileSize, self.tileSize
                )

                if tile == 1:
                    pygame.draw.rect(screen, (255, 223, 0), rect)

                if tile == 2:
                    pygame.draw.rect(screen, (0, 255, 0), rect)

                if tile == 3:
                    pygame.draw.rect(screen, (0, 255, 0), rect)

                if tile == 4:
                    pygame.draw.rect(screen, (255, 0, 0), rect)

                if tile == 5:
                    pygame.draw.rect(screen, (105, 105, 105), rect)

                pygame.draw.rect(screen, (0, 0, 0), rect, width=1)