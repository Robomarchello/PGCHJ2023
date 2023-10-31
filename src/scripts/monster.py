import pygame
from pygame.locals import *
from random import randint
from .pathfinder import find_path
from math import sin


class Monster:
    def __init__(self, player, tile_pos, tileSize, tiles):
        self.tileSize = tileSize
        self.tiles = tiles
        self.prev_pos = tile_pos
        self.tile_pos = tile_pos

        self.player = player
        
        self.roam_target = self.get_target(tiles)

        self.step = 0.2
        self.step_timer = 0

        self.targets = {
            'player': True,
            'roam': False
        }

        #self.rotation = sin(...)

    def move(self, dt):
        player_rect = self.player.rect
        player_tile = (
            (player_rect.x // self.tileSize),
            (player_rect.y // self.tileSize)
        )
        if self.targets['player']:
            target_tile = player_tile

            if self.tiles[player_tile[1]][player_tile[0]] != 0:
                target_tile = self.roam_target
        
        if self.tile_pos == self.roam_target:
            self.roam_target = self.get_target(self.tiles)

        if self.targets['roam']:
            target_tile = self.roam_target

        self.step_timer += (dt / 60)
        if self.step_timer > self.step:
            path = find_path(self.tile_pos, target_tile, self.tiles, [0])
            
            if path != None:
                self.prev_pos = self.tile_pos
                self.tile_pos = path[0]
            else:
                self.prev_pos = self.tile_pos
                
            self.step_timer = 0

    def draw(self, screen, camera_pos):
        interp = self.step_timer / self.step
        new_pos = [
            (self.tile_pos[0] - self.prev_pos[0]) * interp,
            (self.tile_pos[1] - self.prev_pos[1]) * interp
        ]
        new_pos[0] += self.prev_pos[0]
        new_pos[1] += self.prev_pos[1]

        rect = pygame.Rect(
            new_pos[0] * self.tileSize, new_pos[1] * self.tileSize,
            self.tileSize, self.tileSize
        )

        display_rect = rect.copy()
        display_rect.x += camera_pos[0]
        display_rect.y += camera_pos[1]
        pygame.draw.rect(screen, (255, 210, 0), display_rect)

    def get_target(self, tiles):
        roam_target = (
            randint(0, len(tiles[1]) - 1),
            randint(0, len(tiles) - 1)
        )
        while tiles[roam_target[1]][roam_target[0]] != 0:
            roam_target = (
                randint(0, len(tiles[1]) - 1),
                randint(0, len(tiles) - 1)
            )

        return roam_target
