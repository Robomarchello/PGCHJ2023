import pygame
from pygame.locals import *
from src.scripts.mouse import Mouse
from src.scripts.states import *
from src.scripts.audio_handler import AudioHandler
import asyncio

pygame.init()


class App:
    def __init__(self):
        self.ScreenSize = (960, 540)

        self.screen = pygame.display.set_mode(self.ScreenSize)
        pygame.display.set_caption('GAME NAME')

        self.clock = pygame.time.Clock()
        self.fps = 0

        self.dt = 1

        self.states = {
            'game': Game(self.screen, self.ScreenSize, self),
            'jumpscare': (self)
        }
        
        self.crnt_state = 'game'
        self.state = self.states[self.crnt_state]
        
        self.event_handlers = [Mouse]

    async def loop(self):
        screen = self.screen
        while True:
            self.clock.tick(self.fps)
            dt = self.get_dt()

            self.handle_events()
            Mouse.update()
             
            screen.fill((255, 255, 255))

            self.state.draw(dt)

            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.update()

            await asyncio.sleep(0)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            for event_handler in self.event_handlers:
                event_handler.handle_event(event)

            self.state.handle_event(event)
            
    def get_dt(self):
        fps = self.clock.get_fps()

        if fps > 10:
            return (1 / fps) * 60
            
        return 1