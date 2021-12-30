import pygame
from pygame import sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, picturePath):
        super().__init__()
        self.image = pygame.image.load(picturePath)
        self.player_facing_right = pygame.transform.flip(self.image, False, False)
        self.player_facing_left = pygame.transform.flip(self.image, True, False)
        self.player_images = [self.player_facing_right, self.player_facing_left]
        self.rect = self.image.get_rect()
        self.x = int(x)
        self.y = int(y)
        self.velX = 0
        self.left_pressed = False
        self.right_pressed = False
        self.facing_right = True
        self.facing_left = False
        self.speed = 10

    def update(self):
        self.velX = 0

        if self.left_pressed and not self.right_pressed:
            self.velX -= self.speed
            self.facing_right = False
            self.facing_left = True
        if self.right_pressed and not self.left_pressed:
            self.facing_right = True
            self.facing_left = False
            self.velX += self.speed

        if self.facing_right and not self.facing_left:
            self.image = self.player_facing_right
        if self.facing_left and not self.facing_right:
            self.image = self.player_facing_left
        
        self.x += self.velX
        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)