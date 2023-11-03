from .state import State
import pygame
from pygame.locals import *
from src.scripts.mouse import Mouse
from src.scripts.tiles import Level
from src.scripts.player import Player
from src.scripts.monster import Monster
from src.scripts.items import ItemHandler
from src.scripts.oxygen_bar import OxygenBar
from src.scripts.audio_handler import SoundSource, AudioHandler
from src.scripts.message import Messager


class Game(State):
    def __init__(self, screen, ScreenSize, app):
        super().__init__(screen)

        self.ScreenSize = ScreenSize
        self.app = app

        self.tileSize = 50

        self.Messager = Messager('src/assets/font.ttf', self.ScreenSize)

        self.player = Player([480, 270], self.ScreenSize)
        self.ItemHandler = ItemHandler('src/data/items.json', self.player, self.Messager, self)

        self.map = Level('src/data/level1.json', self.ScreenSize, 
                         self.tileSize, self.ItemHandler, self)
        self.monster = Monster(self.player, (32, 32), self.tileSize, self.map.tiles)

        self.OxygenBar = OxygenBar(self.player, self.tileSize, self.map.tiles)

        self.noise = AudioHandler.sounds['noise']
        self.noise.play(-1)
        self.door_snd = AudioHandler.sounds['door']
        monster_sounds = AudioHandler.sounds['zombie']
        self.monster_source = SoundSource(
            monster_sounds, 
            self.player.position, self.monster.real_pos
        )
        self.monster_source.play()
        
        self.vignette = pygame.image.load('src/assets/vignette.png').convert_alpha()

        self.close_trigger = pygame.Rect(0, 700, 750, 100)
        self.closed = False

        self.finish_trigger = pygame.Rect(3050, 0, 100, 100)

        #stats
        self.playtime = 0.0
        self.input_n = 0
        self.deaths = 0

        # TODO: 
        # if windows username == baconinvader
        # then scare him😈😈😈

    def draw(self, dt):
        screen = self.screen

        screen.fill((0, 0, 0))

        self.playtime += dt / 60

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

        self.Messager.draw(screen, dt)

        self.screen.blit(self.vignette, (0, 0))

        player_center = pygame.Vector2(self.player.rect.center)
        monster_center = pygame.Vector2(self.monster.rect.center)

        if self.close_trigger.colliderect(self.player.rect) and not self.closed:
            self.closed = True
            self.Messager.new_message('Why doors closed?', 2)
            self.door_snd.play()

        # Check if game is over
        if (player_center - monster_center).length() < 40 and self.monster.visible:
            self.deaths += 1
            self.app.change_state('game_over')
            self.app.state.reason = 'monster'
            self.monster_source.stop()
            self.noise.stop()

        # game over if ran out of oxygen
        if self.OxygenBar.oxygen_lack:
            self.deaths += 1
            self.app.change_state('game_over')
            self.app.state.reason = 'oxygen'
            self.monster_source.stop()
            self.noise.stop()

        # Check if game is finished
        if self.player.rect.colliderect(self.finish_trigger):
            self.app.change_state('win_screen')
            self.app.state.update_stats(self)
            self.monster_source.stop()
            self.noise.stop()

    def restart(self):
        self.Messager = Messager('src/assets/font.ttf', self.ScreenSize)

        self.player = Player([480, 270], self.ScreenSize)
        self.ItemHandler = ItemHandler('src/data/items.json', self.player, self.Messager, self)

        self.map = Level('src/data/level1.json', self.ScreenSize, 
                         self.tileSize, self.ItemHandler, self)
        self.monster = Monster(self.player, (32, 32), 50, self.map.tiles)

        self.OxygenBar = OxygenBar(self.player, self.tileSize, self.map.tiles)

        self.noise = AudioHandler.sounds['noise']
        self.noise.play(-1)
        monster_sounds = AudioHandler.sounds['zombie']
        self.monster_source = SoundSource(
            monster_sounds, 
            self.player.position, self.monster.real_pos
        )
        self.monster_source.play()

        self.closed = False

    def handle_event(self, event):
        if event.type == KEYDOWN:
            self.input_n += 1

        self.player.handle_event(event)
        self.ItemHandler.handle_event(event)