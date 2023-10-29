import pygame
from pygame.locals import *
from src.scripts.tiles import Level
from src.scripts.pathfinder import find_path
import asyncio
import time

pygame.init()


class App:
    ScreenSize = (960, 540)

    screen = pygame.display.set_mode(ScreenSize)
    pygame.display.set_caption('GAME NAME')

    clock = pygame.time.Clock()
    fps = 120

    dt = 1

    event_handlers = []

    map = Level('src/level.json', 30)
    
    start = [2, 2]
    target = [20, 16]

    timer = time.perf_counter()
    
    path = find_path(start, target, map.tiles)
    for tile in path:
        map.tiles[tile[1]][tile[0]] = 4
        
    map.tiles[start[1]][start[0]] = 2
    map.tiles[target[1]][target[0]] = 3

    @classmethod
    async def loop(cls):
        screen = cls.screen
        while True:
            cls.clock.tick(cls.fps)
            dt = cls.get_dt()

            cls.handle_events()

            screen.fill((255, 255, 255))

            cls.map.draw(screen)

            pygame.display.set_caption(str(cls.clock.get_fps()))
            pygame.display.update()

            await asyncio.sleep(0)
    
    @classmethod
    def handle_events(cls):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
    @classmethod
    def get_dt(cls):
        fps = cls.clock.get_fps()

        if fps > 10:
            return (1 / fps) * 60
            
        return 1