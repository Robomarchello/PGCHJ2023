from .state import State
import pygame
from pygame.locals import *
from src.scripts.audio_handler import AudioHandler


class WinScreen(State):
    def __init__(self, screen, ScreenSize, app):
        super().__init__(screen)

        self.ScreenSize = ScreenSize
        self.center = [
            ScreenSize[0] // 2,
            ScreenSize[1] // 2
        ]

        self.font = pygame.font.Font('src/assets/font.ttf', 64)

    def draw(self, dt):
        '''
        draw a player walking out of the house/hospital moving on the grass
        fadein some stats like deaths, playtime, made for PGC, by ...'''
        ...
            
    def handle_event(self, event):
        pass