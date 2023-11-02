import pygame

pygame.font.init()


class Messager:
    def __init__(self, fontPath, ScreenSize):
        self.font = pygame.font.Font(fontPath, 48)

        self.center = [
            ScreenSize[0] // 2,
            ScreenSize[1] // 2
        ]

        self.messages = []
        self.new_message('test', 3)

        self.timer = 0.0
        self.fade_max = 0.5

        self.opacity = 0

    def draw(self, screen, dt):
        if self.messages != []:
            message = self.messages[0]
            if self.timer < message[2]:
                self.timer += dt / 60
            else:
                self.messages.pop(0)
                self.timer = 0.0

            if self.timer < self.fade_max:
                self.opacity = (self.timer / self.fade_max) * 255
            
            if self.timer > message[2] - self.fade_max:
                self.opacity = (self.timer - (message[2] - self.fade_max)) 
                self.opacity /= self.fade_max
                self.opacity = (1 - self.opacity) * 255

            text = message[0]
            text.set_alpha(self.opacity)
            
            screen.blit(text, message[1].topleft)

    def new_message(self, message:str, time):
        text = self.font.render(message, True, (0, 0, 0))
        
        rect = text.get_rect()
        rect.centerx = self.center[0]
        rect.y = 420
        
        self.messages.append(
            [text, rect, time]
        )
