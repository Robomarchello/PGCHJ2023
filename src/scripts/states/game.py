from .state import State
import pygame
from pygame.locals import *
from src.scripts.mouse import Mouse
from src.scripts.tiles import Level
from src.scripts.player import Player
from src.scripts.monster import Monster, Follower
from src.scripts.items import ItemHandler
from src.scripts.oxygen_bar import OxygenBar
from src.scripts.audio_handler import SoundSource, AudioHandler


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

        self.noise = AudioHandler.sounds['noise']
        self.noise.play(-1)
        monster_sounds = AudioHandler.sounds['zombie']
        self.monster_source = SoundSource(
            monster_sounds, 
            self.player.position, self.monster.real_pos
        )
        self.monster_source.play()

        #stats
        self.playtime = 0.0
        self.input_n = 0

        self.app = app

        self.vignette = pygame.image.load('src/assets/vignette.png').convert_alpha()

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

        self.monster_source.update(self.monster.real_pos, self.player.position)

        self.screen.blit(self.vignette, (0, 0))

        if (self.player.position - self.monster.real_pos).length() < 50:
            self.app.change_state('game_over')
            self.monster_source.stop()
            self.noise.stop()

    def restart(self):
        pass

    def handle_event(self, event):
        if event.type == KEYDOWN:
            self.input_n += 1

        self.player.handle_event(event)
        self.ItemHandler.handle_event(event)