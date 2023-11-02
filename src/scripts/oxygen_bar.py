import pygame


class OxygenBar:
    def __init__(self, player, tileSize, tiles):
        self.player = player

        self.tiles = tiles
        self.tileSize = tileSize

        # slide up animation
        self.anim = False
        self.max_anim = 0.5
        self.anim_timer = 0.0

        self.vent_time = 5
        self.in_vent = 0.0

        self.rect = pygame.Rect(0, 540, 450, 50)
        self.rect.centerx = 480
        self.y_move = 450 - self.rect.y

        self.anim_rect = self.rect.copy()

    def draw(self, screen):
        pygame.draw.rect(screen, (105, 105, 105), self.anim_rect)

    def update(self, dt):
        tile_pos = [
            int(self.player.position[0] // self.tileSize),
            int(self.player.position[1] // self.tileSize)
        ]
        
        if self.tiles[tile_pos[1]][tile_pos[0]] == 2:
            self.anim = True
        else:
            self.anim = False

        if self.anim:
            if self.anim_timer < self.max_anim:
                self.anim_timer += dt / 60
            
        else:
            if self.anim_timer > 0:
                self.anim_timer -= dt / 60

        new_y = self.rect.y + (self.anim_timer / self.max_anim) * self.y_move
        self.anim_rect.y = new_y