import pygame
from pygame.locals import *
from src.scripts.mouse import Mouse
from src.scripts.states import *
from src.scripts.audio_handler import AudioHandler
import sys
import asyncio

pygame.init()


class App:
    def __init__(self):
        self.ScreenSize = (960, 540)

        self.screen = pygame.display.set_mode(self.ScreenSize, SCALED)
        
        if sys.platform == "emscripten":
            caption = 'The Hospitium'
        else:
            caption = 'The Hospitium - F to toggle fullscreen'

        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()
        self.fps = 0

        self.dt = 1

        self.states = {
            'game': Game(self.screen, self.ScreenSize, self),
            'game_over': GameOver(self.screen, self.ScreenSize, self),
            'win_screen': WinScreen(self.screen, self.ScreenSize, self)
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

            #pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.update()

            await asyncio.sleep(0)

    def change_state(self, state):
        self.crnt_state = state
        self.state = self.states[self.crnt_state]

        if state == 'game':
            self.states[self.crnt_state].restart()

        if state == 'game_over':
            self.states[self.crnt_state].scare(self.screen)

        if state == 'win_screen':
            pass
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    raise SystemExit        
                
                if sys.platform != "emscripten":
                    if event.key == K_f:
                        pygame.display.toggle_fullscreen()
            
            for event_handler in self.event_handlers:
                event_handler.handle_event(event)

            self.state.handle_event(event)
            
    def get_dt(self):
        fps = self.clock.get_fps()

        if fps > 10:
            return (1 / fps) * 60
            
        return 1