from .state import State

from random import choice, randint

import pygame
from pygame.locals import *
from src.scripts.mouse import Mouse
from src.scripts.tiles import Level
from src.scripts.player import Player

pygame.font.init()


class Game(State):
    def __init__(self, screen, ScreenSize):
        super().__init__(screen)

        self.ScreenSize = ScreenSize

        self.map = Level('src/level.json', self.ScreenSize, 50)

        self.player = Player([100, 100], self.ScreenSize)

    def draw(self, dt):
        screen = self.screen

        screen.fill((255, 255, 255))

        self.map.draw(screen, self.player.camera_pos)

        self.player.update(dt)
        self.player.draw(screen)

    def handle_event(self, event):
        self.player.handle_event(event)