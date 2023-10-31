import pygame
from pygame.locals import *
from .pathfinder import find_path


class Monster:
    def __init__(self, player, tile_pos, tileSize, tiles):
        self.tileSize = tileSize
        self.tiles = tiles
        self.tile_pos = tile_pos

        self.player = player

        self.step = 0.2
        self.step_timer = 0

        self.targets = {
            'player': True,
            'random': False
        }

    def move(self, dt):
        if self.targets['player']:
            target_rect = self.player.rect
            target_tile = (
                (target_rect.x // self.tileSize),
                (target_rect.y // self.tileSize)
            )

        self.step_timer += (dt / 60)
        if self.step_timer > self.step:
            path = find_path(self.tile_pos, target_tile, self.tiles, [0])
            if path != None:
                self.tile_pos = path[0]
        
            self.step_timer = 0

    def draw(self, screen, camera_pos):
        rect = pygame.Rect(
            self.tile_pos[0] * self.tileSize, self.tile_pos[1] * self.tileSize,
            self.tileSize, self.tileSize
        )
        display_rect = rect.copy()
        display_rect.x += camera_pos[0]
        display_rect.y += camera_pos[1]
        pygame.draw.rect(screen, (255, 210, 0), display_rect)
