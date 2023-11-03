from pygame import Vector2
import pygame.mixer
from json import load

pygame.mixer.init()


class SoundSource:
    def __init__(self, sound, location, target):
        self.sound = sound
        self.location = Vector2(location)
        self.target = Vector2(target)

        self.start = False
        self.channels = []

        self.up = Vector2(0, -1)

    def update(self, target, location):
        self.target.update(target)
        self.location.update(location)
        diff = self.location - self.target
        distance = diff.length() // 2
        if distance > 255:
            distance = 255
        angle = diff.angle_to(self.up)

        for channel in self.channels:
            channel.set_source_location(angle, distance)

    def play(self):
        self.start = True
        self.channels.append(self.sound.play(-1))

    def stop(self):
        self.start = False
        for channel in self.channels:
            channel.stop()


class AudioHandler:
    sounds = {}
    volumes = []
    with open('src/data/sounds.json') as file:
        data = load(file)
        for path in data:
            volume = data[path]['volume']
            volumes.append(volume)  

            pth = data[path]['sound']
            
            sounds[path] = pygame.mixer.Sound(f'src/sfx/{pth}')
            sounds[path].set_volume(volume)

    @classmethod
    def set_volume(cls, volume):
        for sound in cls.sounds:
            cls.sounds[sound].set_volume(volume)

    # pygame.channel.set_source_location()