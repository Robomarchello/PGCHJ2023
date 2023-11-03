import pygame
from random import uniform


class OxygenBar:
    def __init__(self, player, tileSize, tiles):
        self.player = player

        self.tiles = tiles
        self.tileSize = tileSize

        # slide up animation
        self.anim = False
        self.max_anim = 0.5
        self.anim_timer = 0.0

        self.vent_time = 6
        self.in_vent = 6.0
        
        self.oxygen_lack = False

        self.rect = pygame.Rect(0, 540, 450, 50)
        self.rect.centerx = 480
        self.y_move = 450 - self.rect.y

        self.anim_rect = self.rect.copy()

        self.shake = pygame.Vector2(0, 0)

    def draw(self, screen):
        oxygen_rect = self.anim_rect.copy()
        coef = oxygen_rect.width / self.vent_time
        
        oxygen_rect.width = coef * self.in_vent

        pygame.draw.rect(screen, (105, 105, 105), self.anim_rect)
        pygame.draw.rect(screen, (0, 255, 0), oxygen_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.anim_rect, width=3)

    def update(self, dt):
        tile_pos = [
            int(self.player.position[0] // self.tileSize),
            int(self.player.position[1] // self.tileSize)
        ]
        
        if self.tiles[tile_pos[1]][tile_pos[0]] == 5:
            self.anim = True
        else:
            self.anim = False

        if self.anim:
            if self.anim_timer < self.max_anim:
                self.anim_timer += dt / 60 

            if self.in_vent > 0:
                self.in_vent -= dt / 60
            else:
                self.oxygen_lack = True
            
        else:
            if self.anim_timer > 0:
                self.anim_timer -= dt / 60

            if self.in_vent < self.vent_time:
                self.in_vent += (dt / 60) * 1.7
                
        new_y = self.rect.y + (self.anim_timer / self.max_anim) * self.y_move
        self.anim_rect.y = new_y

    def calculate_shake(self, magnitude):
        shake = (
            uniform(-magnitude, magnitude), 
            uniform(-magnitude, magnitude)
        )
        return shake