import pygame
from particles import PARTICLE_EFFECT
from tile import Tile
from settings import *
from player import *

class LEVEL:
    def __init__(self, game_Map, surf):
        #LevelSetup
        self.displaySurf = surf #Assings displaySurf to passed arg surf
        self.setupMap(game_Map) #Calls the setupMap method with arg gameMap
        self.worldShift = 0 #Amount to shift to the world
        self.currentX = 0
        
        #Dust
        self.dustSpt = pygame.sprite.GroupSingle()
        self.playerONGND = False
    
    def jumpParticle(self, pos):
        if self.player.sprite.FR:
            pos -= pygame.math.Vector2(1, 5)
        else:
            pos += pygame.math.Vector2(1, -5)
        jumpPTCL = PARTICLE_EFFECT(pos, 'jump')
        self.dustSpt.add(jumpPTCL)
    
    def isPlayerOnGND(self):
        if self.player.sprite.onGND:
            self.playerONGND = True
        else:
            self.playerONGND = False
    
    def landingParticle(self):
        if not self.playerONGND and self.player.sprite.onGND and not self.dustSpt.sprites():
            if self.player.sprite.FR:
                offset = pygame.math.Vector2(1, 4)
            else:
                offset = pygame.math.Vector2(-1, 4)
            fallPTCL = PARTICLE_EFFECT(self.player.sprite.rect.midbottom - offset, 'land')
            self.dustSpt.add(fallPTCL)
    
    def setupMap(self, layout):
        self.tiles = pygame.sprite.Group() #Assings tiles to pygame sprite group
        self.player = pygame.sprite.GroupSingle() #Assings the player in a pygame groupSingle
        for rowIndex, row in enumerate(layout): #Gets the rowIndex, and row in the gameMap
            for colIndex, tile in enumerate(row): #Gets the colIndex, and tile in the gameMap
                x = colIndex * TILE_SIZE #Assings X as the colIndex times the tile size
                y = rowIndex * TILE_SIZE #Assings Y as the rowIndex times the tile size
                if tile == '1': #If the tile is grass
                    tile = Tile(1, (x,y), TILE_SIZE)
                    self.tiles.add(tile)
                if tile == '2':
                    tile = Tile(2, (x,y), TILE_SIZE)
                    self.tiles.add(tile)
                if tile == 'P':
                    player = PLAYER((x,y), self.displaySurf, self.jumpParticle)
                    self.player.add(player)

    def scrollX(self):
        player = self.player.sprite #Local var assigned to PLAYER
        playerX = player.rect.centerx #Assings local var playerX to the center of the PLAYER
        directionX = player.direction.x #Assings local var directionX to the direction of the PLAYER
        if player.rect.x < ASCREEN_WIDTH / 4 and player.direction.x < 0: #See if the player is below 50p and if they are moving left
            self.worldShift = 2
            player.speed = 0
        elif player.rect.x > ASCREEN_WIDTH - (ASCREEN_WIDTH / 4) and player.direction.x > 0: #See if the player is above 100p and if they are moving right
            self.worldShift = -2
            player.speed = 0
        else: #Stop moving
            self.worldShift = 0
            player.speed = 2

    def Hcollisions(self):
        player = self.player.sprite #Local var player assinged to player sprite
        player.rect.x += player.direction.x * player.speed #Moves the player
        for sprite in self.tiles.sprites(): #Gets each tile
            if sprite.rect.colliderect(player.rect): #Checks if the player has collided with a tile
                if player.direction.x < 0: #If the player is moving Left
                    player.rect.left = sprite.rect.right #Assings the left of the player to the right of the tile
                    player.onL = True
                    self.currentX = player.rect.left
                elif player.direction.x > 0: #If the player is moving right
                    player.rect.right = sprite.rect.left #Assings the right of the player to the left of the tile
                    player.onR = True
                    self.currentX = player.rect.right

        if player.onL and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onL = False
        if player.onR and (player.rect.right > self.currentX or player.direction.x <= 0):
            player.onR = False
        
    def Vcollisions(self):
        player = self.player.sprite #Local var player assinged to player sprite
        player.rect.x += player.direction.y * player.speed #Moves the player
        player.applyGravity() #Start gravity
        for sprite in self.tiles.sprites(): #Gets each tile
            if sprite.rect.colliderect(player.rect): #Checks if the player has collied with a tile
                if player.direction.y > 0: #If the player is going down
                    player.rect.bottom = sprite.rect.top #Assings the player bottom to the top of the tile
                    player.direction.y = 0 #Canecl out gravity
                    player.onGND = True
                elif player.direction.y < 0: #If the player if going up
                    player.rect.top = sprite.rect.bottom #Assings the player top to the bottom of the tile
                    player.direction.y = 0#Cancel out the gravity
                    player.onCLG = True

        if player.onGND and player.direction.y < 0 or player.direction.y > 1:
            player.onGND = False
        if player.onCLG and player.direction.y > 0:
            player.onCLG = False

    def run(self):
        #Dust
        self.dustSpt.update(self.worldShift)
        self.dustSpt.draw(self.displaySurf)
        
        #Level Tiles
        self.tiles.update(self.worldShift) #args shiftX returns None
        self.tiles.draw(self.displaySurf) #args Surface returns list
        self.scrollX()#args None returns None
        
        #Player
        self.player.update() #args None returns None
        self.player.draw(self.displaySurf) #args Surface returns list
        self.Hcollisions() #Start the collisions
        self.isPlayerOnGND()
        self.Vcollisions()
        self.landingParticle()
