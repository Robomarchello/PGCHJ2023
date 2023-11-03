import pygame
from json import load


def load_spritesheet(path, sprite_size):
    image = pygame.image.load(path).convert_alpha()
    image_size = image.get_size()
    sprite_n = (image_size[0] // sprite_size[0],
                image_size[1] // sprite_size[1])
    
    sprites = []
    for y in range(sprite_n[1]):
        for x in range(sprite_n[0]):
            position = (
                -x * sprite_size[0],
                -y * sprite_size[1]
            )
            surf = pygame.Surface(sprite_size)

            surf.blit(image, position)

            sprites.append(surf)

    return sprites


def spritesheet_from_file(filePath):
    with open(filePath) as file:
        data = load(file)

    image = pygame.image.load(data['path']).convert_alpha()
    images = data['tiles'].keys()
    
    sprites = {}
    for sprite in images:
        rect = pygame.Rect(data['rect'])
        rect.x *= -1
        rect.y *= -1

        surf = pygame.Surface(rect.size)
        surf.blit(image, rect.topleft)
        
        sprites[sprite] = surf

    return sprites