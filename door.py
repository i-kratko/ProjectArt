import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, picturePath):
        super().__init__()
        self.image = pygame.image.load(picturePath)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*2), (int(self.size[1]*2))))
        self.x = int(x)
        self.y = int(y)
        self.rect.x = self.x
        self.rect.y = self.y
    
    def interact(self):
        print("Door")