import pygame

class Message():
    def __init__(self, message, color):
        self.fontStyle = pygame.font.SysFont(None, 50)
        self.color = color
        self.message = self.fontStyle.render(message, True, self.color)

    def getMessage(self):
        return self.message