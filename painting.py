import pygame
import const

class Painting(pygame.sprite.Sprite):
    def __init__(self, x, y, interactionMessage, picturePath):
        super().__init__()
        self.image = pygame.image.load(picturePath)
        self.rect = self.image.get_rect()
        self.interactionMessage = interactionMessage
        self.x = int(x)
        self.y = int(y)
        self.rect.x = self.x
        self.rect.y = self.y

    def interact(self):
        self.fontStyle = pygame.font.SysFont(None, 50)
        self.message = self.fontStyle.render(self.interactionMessage, True, const.WHITE)

    def getInteractionMessage(self):
        return self.message
        
        