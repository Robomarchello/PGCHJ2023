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

        self.real_pos = tile_pos
        self.rect = pygame.Rect(self.real_pos, (self.tileSize, self.tileSize))

        self.player = player
        
        self.roam_target = self.get_target(tiles)

        self.step = 0.16
        self.step_timer = 0

        self.visible = False

        self.targets = {
            'player': False,
            'roam': False,
            'still': True
        }

        self.sprite = pygame.image.load('src/assets/monster.png').convert_alpha()
        self.rotation = 0
        self.counter = 0

    def update(self, dt):
        self.counter += dt / 10
        self.rotation = sin(self.counter) * 15
        
        # move & interpolate monster
        player_rect = self.player.rect
        player_tile = (
            (player_rect.x // self.tileSize),
            (player_rect.y // self.tileSize)
        )

        self.step_timer += (dt / 60)
        if self.step_timer > self.step and not self.targets['still']:
            if self.targets['player']:
                target_tile = player_tile

                if not self.tiles[player_tile[1]][player_tile[0]] in [4]:
                    target_tile = self.roam_target
            
            if self.tile_pos == self.roam_target:
                self.roam_target = self.get_target(self.tiles)

            if self.targets['roam']:
                target_tile = self.roam_target
            
            path = find_path(self.tile_pos, target_tile, self.tiles, [4])

            
            if path != None:
                self.prev_pos = self.tile_pos
                self.tile_pos = path[0]
            else:
                target_tile = self.roam_target
                self.prev_pos = self.tile_pos
            
            self.step_timer = 0

        self.real_pos = [
            self.tile_pos[0] * self.tileSize,
            self.tile_pos[1] * self.tileSize
        ]
        self.rect.topleft = self.real_pos

        self.move_dir = [0, 0]
        self.up = pygame.Vector2(0, -1)

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

        diff = pygame.Vector2(self.tile_pos) - self.prev_pos
        angle = diff.angle_to(self.up)
        rightAngle = (angle // 90) * 90
        new_angle = self.rotation + rightAngle - 180
        rotated = pygame.transform.rotate(self.sprite, new_angle)
        rotatedRect = rotated.get_rect(center=display_rect.center)

        if self.visible:
            screen.blit(rotated, rotatedRect)
        
    def target_player(self):
        self.targets = {
            'player': True,
            'roam': False,
            'still': False
        }

    def get_target(self, tiles):
        roam_target = (
            randint(0, len(tiles[1]) - 1),
            randint(0, len(tiles) - 1)
        )
        
        while not tiles[roam_target[1]][roam_target[0]] in [4]:
            roam_target = (
                randint(0, len(tiles[1]) - 1),
                randint(0, len(tiles) - 1)
            )

        return roam_target


class Follower:
    def __init__(self, position, radius, image, target, targetRadius):
        self.position = pygame.Vector2(position)
        self.radius = radius
        self.image = image
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = self.position #self.image.get_rect(topleft=self.position)

        self.target = pygame.Vector2(target)
        self.targetRadius = targetRadius

        self.speed = 4
    
    def update(self, target, dt, tileRects):
        self.target.update(target)

        diff = (self.target - self.position)
        if diff.xy != (0, 0):
            diff_norm = diff.normalize()

            if diff.length() - self.radius - self.targetRadius > 0:
                self.position += diff_norm * self.speed * dt

            if diff.length() > 350:
                self.position = self.target.copy()

        self.rect.center = self.position
        for rect in tileRects:
            if self.rect.colliderect(rect):
                diff = pygame.Vector2(self.rect.center) - rect.center
                if diff.xy != (0, 0):
                    diff_norm = diff.normalize() * 2
                    self.position += diff_norm
                    self.rect.center = self.position

    def draw(self, screen, cam_pos):
        display_pos = self.position.copy()
        display_pos += cam_pos

        pygame.draw.circle(screen, (0, 255, 0), display_pos, self.radius)
