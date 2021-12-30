import pygame

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, picturePath):
        super().__init__()
        self.image = pygame.image.load(picturePath)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.x = int(x)
        self.y = int(y)
        self.rect.x = self.x
        self.rect.y = self.y

    def interact(self):
        print("Key")