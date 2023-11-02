from .state import State
import pygame
from pygame.locals import *
from src.scripts.mouse import Mouse
from src.scripts.tiles import Level
from src.scripts.player import Player
from src.scripts.monster import Monster, Follower
from src.scripts.items import ItemHandler
from src.scripts.oxygen_bar import OxygenBar


class Game(State):
    def __init__(self, screen, ScreenSize, app):
        super().__init__(screen)

        self.ScreenSize = ScreenSize

        tileSize = 50

        self.player = Player([480, 270], self.ScreenSize)
        self.ItemHandler = ItemHandler('src/data/items.json', self.player)

        self.map = Level('src/data/level1.json', self.ScreenSize, tileSize, self.ItemHandler)
        self.monster = Monster(self.player, (2, 2), 50, self.map.tiles)
        
        n_follow = 3
        self.followers = []
        for follow_i in range(n_follow):
            follower = Follower(
            (100, 100), 20, None, self.monster.real_pos, 30)
            self.followers.append(follower)

        self.OxygenBar = OxygenBar(self.player, tileSize, self.map.tiles)

        #stats
        self.playtime = 0.0
        self.input_n = 0

        # if windows username == baconinvader
        # then scare him😈😈😈
        
    def draw(self, dt):
        screen = self.screen

        screen.fill((255, 255, 255))

        self.playtime += dt

        self.player.update(dt, self.map.tileRects)
        self.monster.update(dt)
        self.player.calculate_shake(self.monster)
        self.OxygenBar.update(dt)

        self.map.draw(screen, self.player.camera_pos, dt)
        
        self.ItemHandler.draw(screen, self.player.camera_pos) 
        self.player.draw(screen)
        self.monster.draw(screen, self.player.camera_pos)

        self.OxygenBar.draw(screen)

        if (self.player.position - self.monster.real_pos).length() < 50:
            print('game over')

    def restart(self):
        pass

    def handle_event(self, event):
        if event.type == KEYDOWN:
            self.input_n += 1

        self.player.handle_event(event)
        self.ItemHandler.handle_event(event)