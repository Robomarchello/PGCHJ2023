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
        self.mouse_move *= 0.15
    
    def update(self, dt, tileRects):
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
            velocity = moveVec.normalize() * self.speed * dt

            self.move_player(velocity, tileRects)

        mouse_offset = (Mouse.position - self.center).elementwise() * self.mouse_move

        self.camera_pos = self.center - self.rect.center
        self.camera_pos -= mouse_offset

    def draw(self, screen):
        display_rect = self.rect.copy()
        display_rect.x += self.camera_pos[0]
        display_rect.y += self.camera_pos[1]
        pygame.draw.rect(screen, (255, 0, 0), display_rect)

    def get_collide(self, rect, tileRects):
        collided = []
        for tileRect in tileRects:
            if tileRect.colliderect(rect):
                collided.append(tileRect)
        
        return collided
    
    def move_player(self, velocity, rects):
        self.position[0] += velocity[0]
        self.rect.x = self.position[0]
        collisions = self.get_collide(self.rect, rects)
        for collision in collisions:
            if velocity[0] > 0:
                self.rect.right = collision.left
                self.position[0] = self.rect.x

            if velocity[0] < 0:
                self.rect.left = collision.right
                self.position[0] = self.rect.x

        self.position[1] += velocity[1]
        self.rect.y = self.position[1]
        collisions = self.get_collide(self.rect, rects)
        for collision in collisions:
            if velocity[1] > 0:
                self.rect.bottom = collision.top
                self.position[1] = self.rect.y

            if velocity[1] < 0:
                self.rect.top = collision.bottom
                self.position[1] = self.rect.y

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
        