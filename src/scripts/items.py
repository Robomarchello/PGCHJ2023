import pygame
from pygame.locals import *
from json import load
from random import choice
from .audio_handler import AudioHandler


class Item:
    def __init__(self, position, image, name):
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.name = name

    def draw(self, screen, cam_pos):
        display_rect = self.rect.copy()
        display_rect.x += cam_pos[0]
        display_rect.y += cam_pos[1]
        
        screen.blit(self.image, display_rect.topleft)


class ItemHandler:
    def __init__(self, filePath, player):
        with open(filePath) as file:
            data = load(file)
        
        itemNames = data.keys()

        self.items = []
        for name in itemNames:
            image = pygame.image.load(data[name]["image"]).convert_alpha()
            item = Item(data[name]["position"], image, name)
            self.items.append(item)

        self.player = player

        self.open_exit = False

        self.pickup_sounds = [
            AudioHandler.sounds['pickup1'],
            AudioHandler.sounds['pickup2'],
            AudioHandler.sounds['pickup3']
        ]

    def draw(self, screen, cam_pos):
        for item in self.items:
            item.draw(screen, cam_pos)
 
    def finish(self):
        if len(self.items) == 0:
            print('go to the exit door')
            self.open_exit = True

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_e:
                for item in self.items:
                    if self.player.rect.colliderect(item.rect):
                        self.items.remove(item)

                        choice(self.pickup_sounds).play()

                    self.finish()
