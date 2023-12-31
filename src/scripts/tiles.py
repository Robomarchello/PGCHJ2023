import pygame
from .spritesheet import spritesheet_from_file
from json import load


class Level:
    def __init__(self, path, ScreenSize, tileSize, itemHandler, game):
        self.screenRect = pygame.Rect((0, 0), ScreenSize)
        with open(path) as file:
            self.tiles = load(file)['level']

        self.tileSize = tileSize
        self.tileRects = []

        self.itemHandler = itemHandler
        self.game = game

        self.floor = pygame.image.load('src/assets/floor.png').convert()
        self.grass = pygame.image.load('src/assets/grass.png').convert()
        self.wall = pygame.image.load('src/assets/wall.png').convert()
        self.vent_texture = pygame.image.load('src/assets/vents.png').convert()

        #self.tile_map = pygame.image.load('src/assets/tile_map.png')
        #self.tile_map = spritesheet_from_file('src/data/tiles.json')
        
        self.vents = False
        self.start_anim = True
        self.max_anim = 1.5
        self.vent_anim = 0.0

    def draw(self, screen, offset, dt):
        if self.start_anim:
            if self.vent_anim < self.max_anim:
                self.vent_anim += dt / 60
                self.alpha = (self.vent_anim / self.max_anim) * 255
            else:
                self.vents = True
        else:
            self.vents = False
            self.vent_anim = 0.0
            

        # --- looping through tiles
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
                
                # wall
                if tile == 1:
                    pygame.draw.rect(screen, (105, 105, 105), display_rect)
                    screen.blit(self.wall, display_rect.topleft)
                    self.tileRects.append(rect)

                # grass
                if tile == 2:
                    screen.blit(self.grass, display_rect.topleft)

                # unwalkable grass
                if tile == 3:
                    self.tileRects.append(rect)
                    screen.blit(self.grass, display_rect.topleft)

                # floor
                if tile == 4:
                    screen.blit(self.floor, display_rect.topleft)
                
                # vents
                if tile == 5:
                    pygame.draw.rect(screen, (34, 32, 52), display_rect)

                # exit door                
                if tile == 6:
                    if not self.itemHandler.open_exit:
                        self.tileRects.append(rect)
                    
                        pygame.draw.rect(screen, ((125, 35, 0)), display_rect) 
                    else:  
                        pygame.draw.rect(screen, ((150, 60, 0)), display_rect) 
                    
                    pygame.draw.rect(screen, ((125, 35, 0)), display_rect) 

                # unwalkable for monster
                if tile == 7:
                    screen.blit(self.floor, display_rect.topleft)

                if tile == 8:
                    if self.game.closed:
                        self.tileRects.append(rect)
                    
                        pygame.draw.rect(screen, ((125, 35, 0)), display_rect) 
                    else:  
                        pygame.draw.rect(screen, ((150, 60, 0)), display_rect) 