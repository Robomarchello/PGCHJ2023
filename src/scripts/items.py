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

        black = pygame.mask.from_surface(self.image)
        black = black.to_surface()
        self.blurred = pygame.transform.invert(black)
        self.blurred = pygame.transform.gaussian_blur(self.blurred, 5)
        
        self.blurred.set_alpha(150)
        self.blurred_rect = self.blurred.get_rect()

    def draw(self, screen, cam_pos):
        display_rect = self.rect.copy()
        display_rect.x += cam_pos[0]
        display_rect.y += cam_pos[1]
        
        blurred_rect = display_rect.copy()

        screen.blit(self.blurred, blurred_rect.topleft)
        screen.blit(self.image, display_rect.topleft)


class ItemHandler:
    def __init__(self, filePath, player, messager, game):
        with open(filePath) as file:
            data = load(file)
        
        self.itemNames = data.keys()

        self.items = []
        for name in self.itemNames:
            image = pygame.image.load(data[name]["image"]).convert_alpha()
            item = Item(data[name]["position"], image, name)
            self.items.append(item)

        self.player = player
        self.messager = messager
        self.game = game

        self.open_exit = True

        self.alert_snd = AudioHandler.sounds['alert']
        self.pickup_sounds = [
            AudioHandler.sounds['pickup1'],
            AudioHandler.sounds['pickup2'],
            AudioHandler.sounds['pickup3']
        ]

        self.pickup_text = pygame.image.load('src/assets/pickup_text.png').convert_alpha()
        self.text_rect = self.pickup_text.get_rect()
        self.text_rect.centerx = 480
        self.text_rect.y = 485
        self.scale_length = 120

    def draw(self, screen, cam_pos):
        for item in self.items:
            item.draw(screen, cam_pos)

        for item in self.items:
            player_center = pygame.Vector2(self.player.rect.center)
            diff = player_center - item.rect.center
            length = diff.length()

            if length < self.scale_length:
                closeness = 1 - (length / self.scale_length) ** 2
                scaled_rect = self.text_rect.copy()
                scaled_rect.width *= closeness
                scaled_rect.height *= closeness
                scaled_rect.center = self.text_rect.center
                scaled_image = pygame.transform.scale(
                    self.pickup_text, scaled_rect.size)
                
                screen.blit(scaled_image, scaled_rect.topleft)

    def finish(self):
        if len(self.items) == 0:
            print('go to the exit door')
            self.open_exit = True

    def on_pickup(self, item):
        self.items.remove(item)

        picked_up = len(self.itemNames) - len(self.items)
        if picked_up == len(self.itemNames):            
            self.messager.new_message(
                f'Go to the exit door', 10.0
            )
        else:
            self.messager.new_message(
                f'picked up {picked_up}/{len(self.itemNames)}', 3.0
            )
        
        if picked_up == 1:
            self.game.monster.visible = True
            self.game.monster.target_player()
            self.alert_snd.play()
        
        choice(self.pickup_sounds).play()

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_e:
                for item in self.items:
                    if self.player.rect.colliderect(item.rect):
                        self.on_pickup(item)

                    self.finish()
