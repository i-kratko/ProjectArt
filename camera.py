import pygame
import const

vec = pygame.math.Vector2

class Camera():
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offsetFloat = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = const.disW, const.disH
        self.CONST = vec(-self.DISPLAY_W / 2 + player.rect.w / 2, -self.player.y + 20)
    
    def scroll(self):
        self.offsetFloat.x += (self.player.rect.x - self.offsetFloat.x + self.CONST.x)
        self.offsetFloat.y += (self.player.rect.y - self.offsetFloat.y + self.CONST.y)
        self.offset.x, self.offset.y = int(self.offsetFloat.x), int(self.offsetFloat.y)