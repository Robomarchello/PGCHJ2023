import pygame
from pygame.locals import *
from src.scripts.tiles import Level
from src.scripts.pathfinder import find_path
from src.scripts.player import Player
from src.scripts.mouse import Mouse
from src.scripts.states.state import State
from src.scripts.states.game import Game 
import asyncio


pygame.init()


class App:
    ScreenSize = (960, 540)

    screen = pygame.display.set_mode(ScreenSize)
    pygame.display.set_caption('GAME NAME')

    clock = pygame.time.Clock()
    fps = 0

    dt = 1

    states = {
        'game': Game(screen, ScreenSize)
    }
    
    crnt_state = 'game'
    state = states[crnt_state]
    
    #start = [2, 2]
    #target = [20, 16]
    #path = find_path(start, target, map.tiles)

    event_handlers = [Mouse]

    @classmethod
    async def loop(cls):
        screen = cls.screen
        while True:
            cls.clock.tick(cls.fps)
            dt = cls.get_dt()

            cls.handle_events()
            Mouse.update()
             
            screen.fill((255, 255, 255))

            cls.state.draw(dt)

            pygame.display.set_caption(str(cls.clock.get_fps()))
            pygame.display.update()

            await asyncio.sleep(0)
    
    @classmethod
    def handle_events(cls):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            for event_handler in cls.event_handlers:
                event_handler.handle_event(event)

            cls.state.handle_event(event)
            
    @classmethod
    def get_dt(cls):
        fps = cls.clock.get_fps()

        if fps > 10:
            return (1 / fps) * 60
            
        return 1