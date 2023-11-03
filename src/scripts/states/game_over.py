from .state import State
import pygame
from pygame.locals import *
from random import uniform
from src.scripts.audio_handler import AudioHandler


class GameOver(State):
    def __init__(self, screen, ScreenSize, app):
        super().__init__(screen)

        self.ScreenSize = ScreenSize
        self.center = [
            ScreenSize[0] // 2,
            ScreenSize[1] // 2
        ]

        self.font = pygame.font.Font('src/assets/font.ttf', 64)
        self.restart_text = self.font.render(
            'Press R to restart', True, (255, 255, 255))
        self.restart_rect = self.restart_text.get_rect()
        self.restart_rect.centerx = self.center[0]
        self.restart_rect.y = 400

        self.sound = AudioHandler.sounds['scare_snd']
        self.screen = screen
        self.last_screen = screen.copy()

        self.channel = None

        self.jump_scare = pygame.image.load('src/assets/jumpscare.png').convert()
        self.vents_scare = pygame.image.load('src/assets/jumpscare.png').convert()

        self.scare_rect = self.jump_scare

        self.reasons = [
            'monster', 'oxygen'
        ]
        self.reason = 'monster'

        self.shake = pygame.Vector2(0, 0)
        self.magnitude = 5

        self.app = app

    def scare(self, screen):
        if self.reason == 'monster':
            self.channel = self.sound.play()
            
            self.last_screen = screen.copy()

        elif self.reason == 'oxygen':
            self.channel = self.sound.play()
            
            self.last_screen = screen.copy()

    def draw(self, dt):
        self.calculate_shake(self.magnitude)
        if not self.channel.get_busy():
            self.screen.fill((0, 0, 0))

            self.screen.blit(self.restart_text, self.restart_rect.topleft)

        else:
            rect_new = self.jump_scare.get_rect(center=self.center)
            self.calculate_shake(self.magnitude)
            rect_new.x += self.shake[0]
            rect_new.y += self.shake[1]

            self.screen.blit(self.jump_scare, rect_new.topleft)

    def calculate_shake(self, magnitude):
        self.shake.update(
            uniform(-magnitude, magnitude), 
            uniform(-magnitude, magnitude)
        )

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_r:
                self.app.change_state('game')
