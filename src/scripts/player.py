import pygame
from pygame.locals import *
from .mouse import Mouse


class Player:
    def __init__(self, position, ScreenSize):
        self.position = pygame.Vector2(position)
        self.camera_pos = [0, 0]
        self.rect = pygame.Rect(self.position, (45, 45))

        self.speed = 5
        self.move_dir = {
            'left': False, 'right': False, 'up': False, 'down': False
        }

        self.center = pygame.Vector2(
            ScreenSize[0] // 2,
            ScreenSize[1] // 2
        )
        self.mouse_move = pygame.Vector2(
            ScreenSize[1] / ScreenSize[0],
            1)
        self.mouse_move *= 0.1
    
    def update(self, dt):
        moveVec = pygame.Vector2(0, 0)
        if self.move_dir['left']:
            moveVec[0] = -1
        if self.move_dir['right']:
            moveVec[0] = 1

        if self.move_dir['up']:
            moveVec[1] = -1
        if self.move_dir['down']:
            moveVec[1] = 1

        if moveVec.xy != (0, 0):
            self.position += moveVec.normalize() * self.speed * dt

        mouse_offset = (self.center - Mouse.position).elementwise() * self.mouse_move

        self.camera_pos = [
            -self.position[0],
            -self.position[1]
        ]
        self.camera_pos -= mouse_offset
        
        
        self.rect.center = self.center
        self.rect.topleft += self.position
        self.rect.topleft += self.camera_pos
        #self.rect.topleft -= mouse_offset

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.move_dir['left'] = True
                self.move_dir['right'] = False
            
            if event.key == K_d:
                self.move_dir['right'] = True
                self.move_dir['left'] = False

            if event.key == K_w:
                self.move_dir['up'] = True
                self.move_dir['down'] = False
            
            if event.key == K_s:
                self.move_dir['down'] = True
                self.move_dir['up'] = False

        if event.type == KEYUP:
            if event.key == K_a:
                self.move_dir['left'] = False
            
            if event.key == K_d:
                self.move_dir['right'] = False

            if event.key == K_w:
                self.move_dir['up'] = False
            
            if event.key == K_s:
                self.move_dir['down'] = False
        