from .state import State
import pygame
from pygame.locals import *
from src.scripts.audio_handler import AudioHandler


class GameOver(State):
    def __init__(self, screen, ScreenSize, app):
        super().__init__(screen)

        self.ScreenSize = ScreenSize

        self.sound = AudioHandler.sounds['scare_snd']
        self.screen = screen
        self.last_screen = screen.copy()

        self.channel = None

        self.jump_scare = pygame.image.load('src/assets/jumpscare.png').convert()

        self.app = app

    def scare(self, screen):
        self.channel = self.sound.play()
        
        self.last_screen = screen.copy()

    def draw(self, dt):
        self.screen.blit(self.last_screen, (0, 0))
        if not self.channel.get_busy():
            self.screen.fill((0, 0, 0))
        else:
            self.screen.blit(self.jump_scare, (0, 0))
            
    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_r:
                print('restart')