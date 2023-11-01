from .state import State
import pygame
from pygame.locals import *
from src.scripts.mouse import Mouse
from src.scripts.tiles import Level
from src.scripts.player import Player
from src.scripts.monster import Monster
from src.scripts.items import ItemHandler

pygame.font.init()


class Game(State):
    def __init__(self, screen, ScreenSize):
        super().__init__(screen)

        self.ScreenSize = ScreenSize

        self.map = Level('src/level.json', self.ScreenSize, 50)

        self.player = Player([480, 270], self.ScreenSize)
        self.monster = Monster(self.player, (2, 2), 50, self.map.tiles)

        self.ItemHandler = ItemHandler('src/items.json', self.player)

        #stats
        self.playtime = 0.0
        self.input_n = 0
        self.mouse_miles = 0

        # if windows username == baconinvader
        # scare him😈😈😈
        
    def draw(self, dt):
        screen = self.screen

        screen.fill((255, 255, 255))

        self.playtime += dt

        self.player.update(dt, self.map.tileRects)
        self.monster.move(dt)

        self.map.draw(screen, self.player.camera_pos)
        
        self.ItemHandler.draw(screen, self.player.camera_pos)
        self.player.draw(screen)
        self.monster.draw(screen, self.player.camera_pos)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            self.input_n += 1

        self.player.handle_event(event)
        self.ItemHandler.handle_event(event)