import pygame
from pygame.locals import *

pygame.init()


class App:
    ScreenSize = (960, 540)

    screen = pygame.display.set_mode(ScreenSize)
    pygame.display.set_caption('GAME NAME')

    clock = pygame.time.Clock()
    fps = 120

    dt = 1

    event_handlers = []

    @classmethod
    def loop(cls):
        screen = cls.screen
        while True:
            cls.clock.tick(cls.fps)
            dt = cls.get_dt()

            cls.handle_events()

            screen.fill((0, 0, 0))

            pygame.display.set_caption(str(cls.clock.get_fps()))
            pygame.display.update()
    
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