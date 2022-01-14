from typing import cast
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
from trigger import Trigger
import saveData

data = {
    'playerPos' : 400,
    'currentLevel' : const.first_gallery,
    'playerHasBlackKey' : "no",
    'guardOneBeaten' : False,
    'guardTwoBeaten' : False,
    'galleryOwnerBeaten' : False    
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
        greekColumn1 = Decoration(920, 419, const.greekColumnSpritePath)
        greekColumn2 = Decoration(1300, 419, const.greekColumnSpritePath)
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
        castle = Painting(315, 350, const.castleInteraction, const.castle)
        newspaper = Painting(500, 350, const.newspaperInteraction, const.newspaper)
        sightseeing = Painting(700, 350, const.sightseeingInteraction, const.sightseeing)
        boxed = Painting(900, 350, const.boxedInteraction, const.boxed)
        astronautInTheOcean = Painting(1100, 350, const.astronautInTheOceanInteraction, const.astronautInTheOcean)
        boat = Painting(1300, 350, const.boatInteraction, const.boat)
        help = Painting(1480, 350, const.helpInteraction, const.help)
        paintingGroup = pygame.sprite.Group()
        paintingGroup.add(castle)
        paintingGroup.add(newspaper)
        paintingGroup.add(sightseeing)
        paintingGroup.add(boxed)
        paintingGroup.add(astronautInTheOcean)
        paintingGroup.add(boat)
        paintingGroup.add(help)

        #doors
        firstGalleryDoor = Door(400, 400, const.whiteDoorPath)
        galleryOwnerOfficeDoor = Door(1380, 400, const.whiteDoorPath)
        doorGroup = pygame.sprite.Group()
        doorGroup.add(firstGalleryDoor)
        doorGroup.add(galleryOwnerOfficeDoor)

        #npcs
        artEnthusiast = NPC(650, 400, const.artEnthusiastInteraction, const.artEnthusiastNPCSpritePath)
        artEnthusiast.flip()
        redHairMan = NPC(1050, 400, const.redHairManInteraction, const.redHairManNPCSpritePath)
        npcGroup = pygame.sprite.Group()
        npcGroup.add(artEnthusiast)
        npcGroup.add(redHairMan)

        #decorations
        flowepot1 = Decoration(325, 435, const.flowerpotSpritePath)
        flowepot2 = Decoration(1490, 435, const.flowerpotSpritePath)
        greekColumn1 = Decoration(600, 419, const.greekColumnSpritePath)
        greekColumn2 = Decoration(800, 419, const.greekColumnSpritePath)
        greekColumn3 = Decoration(1000, 419, const.greekColumnSpritePath)
        greekColumn4 = Decoration(1200, 419, const.greekColumnSpritePath)
        officeSign = Decoration(1380, 275, const.officeSign) 
        decorationsGroup = pygame.sprite.Group()
        decorationsGroup.add(flowepot1)
        decorationsGroup.add(flowepot2)
        decorationsGroup.add(greekColumn1)
        decorationsGroup.add(greekColumn2)
        decorationsGroup.add(greekColumn3)
        decorationsGroup.add(greekColumn4)
        decorationsGroup.add(officeSign)
    

        #messages
        pressSpaceToContinue = Message(const.pressSpaceToContinue, const.WHITE)

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
                                if door == galleryOwnerOfficeDoor:
                                    self.state = const.office
                                    data["playerPos"] = 420
                                    self.stateManager()
                        for npc in npcGroup:
                            if player.rect.colliderect(npc.rect):
                                npc.interact(const.WHITE)
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
            for decoration in decorationsGroup:
                dis.blit(decoration.image, (decoration.rect.x - camera.offset.x, decoration.rect.y - camera.offset.y - const.OFFSETYFORMAPS - 3))
            dis.blit(player.image, (player.rect.x - camera.offset.x, player.rect.y - camera.offset.y - const.OFFSETYFORMAPS))
            pygame.display.update()

            #update save data
            data["playerPos"] = player.rect.x

            clock.tick(const.FPS)
    
    def office(self):
        data["currentLevel"] = const.office
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
        backDoor = Door(400, 400, const.whiteDoorPath)
        doorGroup = pygame.sprite.Group()
        doorGroup.add(backDoor)

        #npcs
        guard1 = NPC(600, 400, const.securityGuardNPC1Interaction, const.securityGuardNPC1SpritePath)
        guard1.flip()
        guard2 = NPC(800, 400, const.securityGuardNPC2Interaction, const.securityGuardNPC2SpritePath)
        guard2.flip()
        galleryOwner = NPC(1050, 380, const.artEnthusiastInteraction, const.galleryOwnerNPCSpritePath)
        galleryOwner.flip()
        npcGroup = pygame.sprite.Group()
        npcGroup.add(guard1)
        npcGroup.add(guard2)
        npcGroup.add(galleryOwner)
        
        #decorations
        officeDesk = Decoration(1000, 404, const.officeDesk)
        decorationsGroup = pygame.sprite.Group()
        decorationsGroup.add(officeDesk)
        
        #messages
        pressSpaceToContinue = Message(const.pressSpaceToContinue, const.WHITE)
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
                                if door == backDoor:
                                    self.state = const.second_gallery
                                    data["playerPos"] = 1400
                                    self.stateManager()
                        for npc in npcGroup:
                            if player.rect.colliderect(npc.rect):
                                npc.interact(const.WHITE)
                                dis.blit(npc.getInteractionMessage(), (0, 0))
                                dis.blit(pressSpaceToContinue.getMessage(), (0, 50))
                                if npc == guard1 and data["guardOneBeaten"] == False:
                                    self.state = const.firstGuardMinigame
                                    data["playerPos"] = player.rect.x
                                    self.stateManager()
                                if npc == guard2 and data["guardTwoBeaten"] == False:
                                    self.state = const.secondGuardMinigame
                                    data["playerPos"] = player.rect.x
                                    self.stateManager()
                                if npc == galleryOwner and data["galleryOwnerBeaten"] == False:
                                    self.state = const.galleryOwnerBossMinigame
                                    data["playerPos"] = player.rect.x
                                    self.stateManager()
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
            for decoration in decorationsGroup:
                dis.blit(decoration.image, (decoration.rect.x - camera.offset.x, decoration.rect.y - camera.offset.y - const.OFFSETYFORMAPS - 3))
            dis.blit(player.image, (player.rect.x - camera.offset.x, player.rect.y - camera.offset.y - const.OFFSETYFORMAPS))

            pygame.display.update()

            #update save data
            data["playerPos"] = player.rect.x
            clock.tick(const.FPS)

    def firstGuardMinigame(self):
        data["currentLevel"] = const.firstGuardMinigame
        gameOver = False
        pause = False
        background = pygame.image.load(const.guardMinigameBackground)
        maze = pygame.image.load(const.firstGuardMinigameMaze).convert_alpha()
        mazeMask = pygame.mask.from_surface(maze)
        mazeRect = maze.get_rect()        

        #player
        player = Player(40, 165, const.mazePlayerSpritePath)
        playerGroup = pygame.sprite.Group()
        playerGroup.add(player)

        #triggers
        endMazeTrigger = Trigger(740, 420, 60, 60)
        triggerGroup = []
        triggerGroup.append(endMazeTrigger)

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
                    elif event.key == pygame.K_d:
                        player.right_pressed = True
                    elif event.key == pygame.K_w:
                        player.up_pressed = True
                    elif event.key == pygame.K_s:
                        player.down_pressed = True
                    if event.key == pygame.K_ESCAPE:
                        self.state = const.main_menu
                        self.stateManager()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        player.left_pressed = False
                    elif event.key == pygame.K_d:
                        player.right_pressed = False
                    elif event.key == pygame.K_w:
                        player.up_pressed = False
                    elif event.key == pygame.K_s:
                        player.down_pressed = False
                for trigger in triggerGroup:
                    if player.rect.colliderect(trigger.rect):
                        if trigger == endMazeTrigger:
                            trigger.defaultTrigger()
                            self.state = const.office
                            data["guardOneBeaten"] = True
                            self.stateManager()

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
            player.mazeMovementUpdate()
            player.dir()
            
            offset = (player.x, player.y)
            result = mazeMask.overlap(player.mask, offset)
            if result:
                player.speed = 0
                player.velX = 0
                player.velY = 0
                dir = player.direction
                if dir == const.facingRight:
                    player.x -= 5
                elif dir == const.facingLeft:
                    player.x += 5
                elif dir == const.facingUp:
                    player.y += 5
                elif dir == const.facingDown:
                    player.y -= 5
                

            dis.blit(background, (0, 0))
            dis.blit(maze, (0, 0))
            dis.blit(player.image, (player.x, player.y))

            for t in triggerGroup:
                dis.blit(t.trigger, (t.x, t.y))

            pygame.display.update()
    
            clock.tick(const.FPS)

    def secondGuardMinigame(self):
        pass

    def galleryOwnerBossMinigame(self):
        pass

    def stateManager(self):
        if self.state == const.main_menu:
            self.mainMenu()
        if self.state == const.first_gallery:
            data["currentLevel"] = const.first_gallery
            self.firstGallery()
        if self.state == const.second_gallery:
            data["currentLevel"] = const.second_gallery
            self.secondGallery()
        if self.state == const.office:
            data["currentLevel"] = const.office
            self.office()
        if self.state == const.firstGuardMinigame:
            data["currentLevel"] = const.firstGuardMinigame
            self.firstGuardMinigame()
        if self.state == const.secondGuardMinigame:
            data["currentLevel"] = const.secondGuardMinigame
            self.secondGuardMinigame()
        if self.state == const.galleryOwnerBossMinigame:
            data["currentLevel"] = const.galleryOwnerBossMinigame
            self.galleryOwnerBossMinigame()
            
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