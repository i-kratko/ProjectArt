import pygame
import const

class Trigger():
    def __init__(self, x, y, w, h):
        self.trigger = pygame.Surface((int(w), int(h)))
        self.trigger.set_alpha(0)
        self.trigger.fill(const.WHITE)
        self.rect = self.trigger.get_rect()
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.rect.x = self.x
        self.rect.y = self.y

        #trigger types
        self.trapTrigger = False

    def defaultTrigger(self):
        print("triggered")

    def makeIntoTrapTrigger(self):
        self.trapTrigger = True

    def disableTrapTrigger(self):
        self.trapTrigger = False