from .state import State
import pygame
from pygame.locals import *
from src.scripts.audio_handler import AudioHandler


class WinScreen(State):
    def __init__(self, screen, ScreenSize, app):
        super().__init__(screen)

        self.screen = screen
        self.ScreenSize = ScreenSize
        self.center = [
            ScreenSize[0] // 2,
            ScreenSize[1] // 2
        ]

        self.font = pygame.font.Font('src/assets/font.ttf', 64)

        self.timer = 0.0
        self.fade_max = 0.5

        self.opacity = 0

        self.messages = []
        self.new_message('Congratulations!', 2)
        self.new_message('You\'ve Escaped!', 3)
        self.new_message(f'You have been \n playing  for N minutes', 3)
        self.new_message(f'You died N times', 3)
        self.new_message('Made in 7 days for PGCHJ2023', 3)
        self.new_message('By RoboMarchello and Boopka', 2)
        self.new_message('Thanks for playing', 5)

        self.finish_snd = AudioHandler.sounds['yippie']

    def draw(self, dt):
        '''
        draw a player walking out of the house/hospital moving on the grass
        fadein some stats like deaths, playtime, made for PGC, by ...
        '''
        if self.messages != []:
            message = self.messages[0]
            if self.timer < message[2]:
                self.timer += dt / 60
            else:
                self.messages.pop(0)
                self.timer = 0.0

            if self.timer < self.fade_max:
                self.opacity = (self.timer / self.fade_max) * 255
            
            if self.timer > message[2] - self.fade_max:
                self.opacity = (self.timer - (message[2] - self.fade_max)) 
                self.opacity /= self.fade_max
                self.opacity = (1 - self.opacity) * 255

            text = message[0]
            text.set_alpha(self.opacity)
            
            self.screen.blit(text, message[1].topleft)

    def update_stats(self, game):
        self.messages = []
        self.finish_snd.play()
        playtime = round(game.playtime / 60, 2)
        self.new_message('Congratulations!', 2)
        self.new_message('You\'ve Escaped!', 3)
        self.new_message(f'You have been \n playing  for {playtime} minutes', 3)
        self.new_message(f'You died {game.deaths} times', 3)
        self.new_message('Made in 7 days for PGCHJ2023', 3)
        self.new_message('By RoboMarchello and Boopka', 2)
        self.new_message('Thanks for playing', 5)

    def new_message(self, message:str, time):
        text = self.font.render(message, True, (0, 0, 0))
        
        rect = text.get_rect()
        rect.centerx = self.center[0]
        rect.y = 200
        
        self.messages.append(
            [text, rect, time]
        )

