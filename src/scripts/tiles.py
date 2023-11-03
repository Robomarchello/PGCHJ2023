import pygame
from json import load


class Level:
    def __init__(self, path, ScreenSize, tileSize, itemHandler):
        self.screenRect = pygame.Rect((0, 0), ScreenSize)
        with open(path) as file:
            self.tiles = load(file)['level']

        self.tileSize = tileSize
        self.tileRects = []

        self.itemHandler = itemHandler

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
                    self.tileRects.append(rect)

                # grass
                if tile == 2:
                    pygame.draw.rect(screen, (0, 100, 0), display_rect)

                # unwalkable grass
                if tile == 3:
                    pygame.draw.rect(screen, (0, 150, 0), display_rect)
                    self.tileRects.append(rect)

                # floor
                if tile == 4:
                    pygame.draw.rect(screen, (180, 180, 180), display_rect)
                
                # vents
                if tile == 5:
                    pygame.draw.rect(screen, (130, 130, 130), display_rect)

                # exit door                
                if tile == 6:
                    pygame.draw.rect(screen, (125, 35, 0), display_rect)
                    if not self.itemHandler.open_exit:
                        self.tileRects.append(rect)

                # unwalkable for monster
                if tile == 7:
                    pygame.draw.rect(screen, (180, 180, 180), display_rect)                

                '''if tile == 1:
                    pygame.draw.rect(screen, (105, 105, 105), display_rect)
                    self.tileRects.append(rect)

                if tile == 2:
                    pygame.draw.rect(screen, (150, 150, 150), display_rect)

                if tile == 4:
                    pygame.draw.rect(screen, (125, 35, 0), display_rect)

                    if not self.itemHandler.open_exit:
                        self.tileRects.append(rect)
                        '''
                pygame.draw.rect(screen, (0, 0, 0), display_rect, width=1)