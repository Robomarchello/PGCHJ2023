from .state import State
import pygame
from pygame.locals import *
from src.scripts.mouse import Mouse
from src.scripts.tiles import Level
from src.scripts.player import Player
from src.scripts.monster import Monster

pygame.font.init()


class Game(State):
    def __init__(self, screen, ScreenSize):
        super().__init__(screen)

        self.ScreenSize = ScreenSize

        self.map = Level('src/level.json', self.ScreenSize, 50)

        self.player = Player([480, 270], self.ScreenSize)
        self.monster = Monster(self.player, (2, 2), 50, self.map.tiles)

    def draw(self, dt):
        screen = self.screen

        screen.fill((255, 255, 255))

        self.player.update(dt, self.map.tileRects)
        self.monster.move(dt)

        self.map.draw(screen, self.player.camera_pos)
        
        self.player.draw(screen)
        self.monster.draw(screen, self.player.camera_pos)

    def handle_event(self, event):
        self.player.handle_event(event)