import pygame
import sys
import const
from os import path
from player import Player
from button import Button
from camera import Camera
from painting import Painting
from message import Message
from door import Door
from npc import NPC
from key import Key
from decoration import Decoration
import saveData

data = {
    'playerPos' : 400,
    'currentLevel' : const.first_gallery,
    'playerHasBlackKey' : "no"
}

data = saveData.loadData("save.txt")

class GameState():
    def __init__(self):
        self.state = const.main_menu

    def mainMenu(self):
        gameOver = False

        background = pygame.image.load(const.backgroundPath)
        startButton = Button((const.disW / 2 - 79), (const.disH / 2 - 22), const.mainMenuStartButtonPath)

        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if startButton.rect.collidepoint(pos):
                        print("start button clicked")
                        self.state = data["currentLevel"]
                        self.stateManager()                     
                
            dis.blit(background, (0, 0))
            dis.blit(startButton.image, (startButton.x, startButton.y))
            pygame.display.update()
            clock.tick(const.FPS)
        

    ##### GALLERY STAGE #####
    def firstGallery(self):
        data["currentLevel"] = const.first_gallery
        gameOver = False
        pause = False
        
        background = pygame.image.load(const.galleryMap)

        #player
        player = Player(f'{data["playerPos"]}', 400, const.playerSpritePath)
        playerGroup = pygame.sprite.Group()
        playerGroup.add(player)

        #paintings
        treeInAField = Painting(400, 350, const.treeInAFieldInteraction, const.treeInAFlied)
        sunsetByTheSea = Painting(600, 350, const.sunsetByTheSeaInteraction, const.sunsetByTheSea)
        snowman = Painting(1000, 350, const.snowmanInteraction, const.snowman)
        mountains = Painting(1200, 350, const.mountainsInteraction, const.mountains)

        paintingGroup = pygame.sprite.Group()
        paintingGroup.add(treeInAField)
        paintingGroup.add(sunsetByTheSea)
        paintingGroup.add(snowman)
        paintingGroup.add(mountains)

        #doors
        secondGalleryDoor = Door(800, 400, const.whiteDoorPath)
        secretGalleryDoor = Door(1400, 400, const.blackDoorPath)
        doorGroup = pygame.sprite.Group()
        doorGroup.add(secondGalleryDoor)
        doorGroup.add(secretGalleryDoor)

        #npcs
        oldManNPC = NPC(500, 400, const.oldManInteraction, const.oldManNPCSpritePath)
        npcGroup = pygame.sprite.Group()
        npcGroup.add(oldManNPC)

        #decorations
        flowepot1 = Decoration(700, 435, const.flowerpotSpritePath)
        flowepot2 = Decoration(1100, 435, const.flowerpotSpritePath)
        greekColumn1 = Decoration(920, 420, const.greekColumnSpritePath)
        greekColumn2 = Decoration(1300, 420, const.greekColumnSpritePath)
        decorationsGroup = pygame.sprite.Group()
        decorationsGroup.add(flowepot1)
        decorationsGroup.add(flowepot2)
        decorationsGroup.add(greekColumn1)
        decorationsGroup.add(greekColumn2)

        #keys
        blackDoorKey = Key(1100, 450, const.blackDoorKeyPath)
        keyGroup = pygame.sprite.Group()
        ##check if player already has the key
        if data["playerHasBlackKey"] == "yes":
            blackDoorKey.destroy()
        else:
            keyGroup.add(blackDoorKey)

        #messages
        pressSpaceToContinue = Message(const.pressSpaceToContinue, const.WHITE)
        pickupKeyMessage = Message(const.pickupKey1, const.WHITE)
        doorLockedMessage = Message(const.doorLocked, const.WHITE)

        #camera
        camera = Camera(player)
        
        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                    saveData.saveData("save.txt", data)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player.left_pressed = True
                    if event.key == pygame.K_d:
                        player.right_pressed = True
                    if event.key == pygame.K_ESCAPE:
                        self.state = const.main_menu
                        self.stateManager()
                    if event.key == pygame.K_q:
                        for painting in paintingGroup:
                            if player.rect.colliderect(painting.rect):
                                painting.interact()
                                dis.blit(painting.getInteractionMessage(), (0, 0))
                                dis.blit(pressSpaceToContinue.getMessage(), (0, 50))
                                pygame.display.update()
                                pause = True
                        for door in doorGroup:
                            if player.rect.colliderect(door.rect):
                                door.interact()
                                if door == secondGalleryDoor:
                                    self.state = const.second_gallery
                                    data["playerPos"] = 410
                                    self.stateManager()
                                if door == secretGalleryDoor and data["playerHasBlackKey"] == "yes":
                                    print("secret door accessed")
                                if door == secretGalleryDoor and data["playerHasBlackKey"] == "no":
                                    print("cant access this door")
                                    dis.blit(doorLockedMessage.getMessage(), (0, 0))
                                    dis.blit(pressSpaceToContinue.getMessage(), (0, 50))
                                    pygame.display.update()
                                    pause = True
                        for npc in npcGroup:
                            if player.rect.colliderect(npc.rect):
                                npc.interact(const.WHITE)
                                dis.blit(npc.getInteractionMessage(), (0, 0))
                                dis.blit(pressSpaceToContinue.getMessage(), (0, 50))
                                pygame.display.update()
                                pause = True    
                        for key in keyGroup:
                            if player.rect.colliderect(key.rect):
                                print("collisionus")
                                key.interact()
                                dis.blit(pickupKeyMessage.getMessage(), (0, 0))
                                dis.blit(pressSpaceToContinue.getMessage(), (0, 50))
                                pygame.display.update()
                                pause = True
                                if key == blackDoorKey:
                                    data["playerHasBlackKey"] = "yes"
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        player.left_pressed = False
                    if event.key == pygame.K_d:
                        player.right_pressed = False
            while pause:
               for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                       gameOver = True
                       pygame.quit()
                       sys.exit()
                   if event.type == pygame.KEYDOWN:
                       if event.key == pygame.K_SPACE:
                           pause = False

            #update display
            player.update()
            camera.scroll()

            dis.blit(background, (0 - camera.offset.x, 0))

            for painting in paintingGroup:
                dis.blit(painting.image, (painting.rect.x - camera.offset.x, painting.rect.y - camera.offset.y))
            for door in doorGroup:
                dis.blit(door.image, (door.rect.x - camera.offset.x, door.rect.y - camera.offset.y - 64 - const.OFFSETYFORMAPS))
            for npc in npcGroup:
                dis.blit(npc.image, (npc.rect.x - camera.offset.x, npc.rect.y - camera.offset.y - const.OFFSETYFORMAPS))
            for key in keyGroup:
                dis.blit(key.image, (key.rect.x - camera.offset.x, key.rect.y - camera.offset.y - const.OFFSETYFORMAPS - 2))
            for decoration in decorationsGroup:
                dis.blit(decoration.image, (decoration.rect.x - camera.offset.x, decoration.rect.y - camera.offset.y - const.OFFSETYFORMAPS - 3))
            dis.blit(player.image, (player.rect.x - camera.offset.x, player.rect.y - camera.offset.y - const.OFFSETYFORMAPS))
            pygame.display.update()

            #update save data
            data["playerPos"] = player.rect.x

            clock.tick(const.FPS)

    def secondGallery(self):
        data["currentLevel"] = const.second_gallery
        gameOver = False
        pause = False
        
        background = pygame.image.load(const.galleryMap)

        #player
        player = Player(f'{data["playerPos"]}', 400, const.playerSpritePath)
        playerGroup = pygame.sprite.Group()
        playerGroup.add(player)

        #paintings
        paintingGroup = pygame.sprite.Group()

        #doors
        firstGalleryDoor = Door(400, 400, const.whiteDoorPath)
        doorGroup = pygame.sprite.Group()
        doorGroup.add(firstGalleryDoor)

        #npcs
        npcGroup = pygame.sprite.Group()

        #messages
        pressSpaceToContinue = Message(const.pressSpaceToContinue, [255, 255, 255])

        #camera
        camera = Camera(player)
        
        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                    saveData.saveData("save.txt", data)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player.left_pressed = True
                    if event.key == pygame.K_d:
                        player.right_pressed = True
                    if event.key == pygame.K_ESCAPE:
                        self.state = const.main_menu
                        self.stateManager()
                    if event.key == pygame.K_q:
                        for painting in paintingGroup:
                            if player.rect.colliderect(painting.rect):
                                painting.interact()
                                dis.blit(painting.getInteractionMessage(), (0, 0))
                                dis.blit(pressSpaceToContinue.getMessage(), (0, 50))
                                pygame.display.update()
                                pause = True
                        for door in doorGroup:
                            if player.rect.colliderect(door.rect):
                                door.interact()
                                if door == firstGalleryDoor:
                                    self.state = const.first_gallery
                                    data["playerPos"] = 820
                                    self.stateManager()
                        for npc in npcGroup:
                            if player.rect.colliderect(npc.rect):
                                npc.interact(const.BLACK)
                                dis.blit(npc.getInteractionMessage(), (0, 0))
                                dis.blit(pressSpaceToContinue.getMessage(), (0, 50))
                                pygame.display.update()
                                pause = True    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        player.left_pressed = False
                    if event.key == pygame.K_d:
                        player.right_pressed = False
                
            while pause:
               for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                       gameOver = True
                       pygame.quit()
                       sys.exit()
                   if event.type == pygame.KEYDOWN:
                       if event.key == pygame.K_SPACE:
                           pause = False

            #update display
            player.update()
            camera.scroll()

            dis.blit(background, (0 - camera.offset.x, 0))

            for painting in paintingGroup:
                dis.blit(painting.image, (painting.rect.x - camera.offset.x, painting.rect.y - camera.offset.y))
            for door in doorGroup:
                dis.blit(door.image, (door.rect.x - camera.offset.x, door.rect.y - camera.offset.y - 64 - const.OFFSETYFORMAPS))
            for npc in npcGroup:
                dis.blit(npc.image, (npc.rect.x - camera.offset.x, npc.rect.y - camera.offset.y - const.OFFSETYFORMAPS))
            dis.blit(player.image, (player.rect.x - camera.offset.x, player.rect.y - camera.offset.y - const.OFFSETYFORMAPS))
            pygame.display.update()

            #update save data
            data["playerPos"] = player.rect.x

            clock.tick(const.FPS)

    def stateManager(self):
        if self.state == const.main_menu:
            self.mainMenu()
        if self.state == const.first_gallery:
            data["currentLevel"] = const.first_gallery
            self.firstGallery()
        if self.state == const.second_gallery:
            data["currentLevel"] = const.second_gallery
            self.secondGallery()
            
#setup
pygame.init()
dis = pygame.display.set_mode((const.disW, const.disH))
pygame.display.update()
pygame.display.set_caption(const.gameName)
stateMachine = GameState()

clock = pygame.time.Clock()

def gameLoop():
    while True:
        stateMachine.stateManager()

#start game loop
gameLoop()