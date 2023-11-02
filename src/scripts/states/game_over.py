from .state import State
import pygame
from pygame.locals import *
from src.scripts.audio_handler import AudioHandler


class GameOver(State):
    def __init__(self, screen, ScreenSize, app):
        super().__init__(screen)

        self.ScreenSize = ScreenSize

        self.sound = AudioHandler.sounds['scare']
        self.last_screen = screen

        self.channel = None

        self.black_time = 3
        self.timer = 0.0

    def scare(self, screen):
        self.channel = self.sound.play()
        
        self.last_screen = screen.copy()

    def draw(self, screen, dt):
        if not self.channel.get_busy():
            screen.fill((0, 0, 0))

            if self.timer < self.black_time:
                self.timer += dt
            else:
                App.crnt_state = 'game'
        else:
            # jump scare
            ...
    def handle_event(self, event):
        pass