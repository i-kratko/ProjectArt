import pygame
from pygame import sprite
import const

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, picturePath):
        super().__init__()
        self.image = pygame.image.load(picturePath).convert_alpha()
        self.player_facing_right = pygame.transform.flip(self.image, False, False)
        self.player_facing_left = pygame.transform.flip(self.image, True, False)
        self.player_images = [self.player_facing_right, self.player_facing_left]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.x = int(x)
        self.y = int(y)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.facing_right = True
        self.facing_left = False
        self.facing_up = False
        self.facing_down = False
        self.direction = ""
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
        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 64)

    #MAZE
    def mazeMovementUpdate(self):
        self.velX = 0
        self.velY = 0
        self.speed = 3

        if self.left_pressed and not self.right_pressed:
            self.velX -= self.speed
            self.facing_up = False
            self.facing_down = False
            self.facing_right = False
            self.facing_left = True
        if self.right_pressed and not self.left_pressed:
            self.velX += self.speed
            self.facing_up = False
            self.facing_down = False
            self.facing_right = True
            self.facing_left = False
        if self.up_pressed and not self.down_pressed:
            self.velY -= self.speed
            self.facing_up = True
            self.facing_down = False
            self.facing_right = False
            self.facing_left = False
        if self.down_pressed and not self.up_pressed:
            self.velY += self.speed
            self.facing_up = False
            self.facing_down = True
            self.facing_right = False
            self.facing_left = False

        if self.facing_right and not self.facing_left:
            self.image = self.player_facing_right
        if self.facing_left and not self.facing_right:
            self.image = self.player_facing_left
        
        self.x += self.velX
        self.y += self.velY
        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 64)

    #dir
    def dir(self):
        if self.facing_right:
            self.direction = const.facingRight
        elif self.facing_left:
            self.direction = const.facingLeft
        if self.facing_up:
            self.direction = const.facingUp
        elif self.facing_down:
            self.direction = const.facingDown
