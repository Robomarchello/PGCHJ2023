import pygame.mixer
from json import load

pygame.mixer.init()


class AudioHandler:
    sounds = {}
    with open('folder_to_enter') as file:
        data = load(file)
        for path in data:
            sounds[path] = {
                'sound': pygame.mixer.Sound(f'src/sfx/{data[path]}'),
                'volume': data['volume']
                } 

    @classmethod
    def set_volume(cls, volume):
        for sound in cls.sounds:
            cls.sounds[sound].set_volume(volume)

    # pygame.channel.set_source_location()