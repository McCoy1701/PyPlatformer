import pygame
from tiles import TILE, STATIC_TILE, CRATE, COIN, TREE
from support import IMPORT_CSV, IMPORT_GRAPHICS
from enemy import ENEMY
from decoration import SKY, WATER, CLOUD
from player import PLAYER
from particles import PARTICLE_EFFECT
from settings import *

class LEVEL:
    def __init__(self, levelData, surf):
        self.worldShift = 0
        self.displaySurf = surf
        self.currentX = None

        playerLayout = IMPORT_CSV(levelData['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.playerSetup(playerLayout)

        self.dustSprite = pygame.sprite.GroupSingle()
        self.playerOnGround = False

        self.makeSprites(levelData)

        self.sky = SKY(13)
        lvlWidth = len(IMPORT_CSV(levelData['terrain'])[0]) * TILE_SIZE
        self.water = WATER(ASCREEN_HEIGHT - 8,  lvlWidth)
        self.clouds = CLOUD(100, lvlWidth, 40)

    def makeSprites(self, levelData):
        self.terrainSprites = self.createTileGroup(IMPORT_CSV(levelData['terrain']), 'terrain')
        self.grassSprites = self.createTileGroup(IMPORT_CSV(levelData['grass']), 'grass')
        self.crateSprites = self.createTileGroup(IMPORT_CSV(levelData['crates']), 'crates')
        self.coinSprites = self.createTileGroup(IMPORT_CSV(levelData['coins']), 'coins')
        self.FGTreeSprites = self.createTileGroup(IMPORT_CSV(levelData['FGTrees']), 'FGTrees')
        self.BGTreeSprites = self.createTileGroup(IMPORT_CSV(levelData['BGTrees']), 'BGTrees')
        self.enemySprites = self.createTileGroup(IMPORT_CSV(levelData['enemies']), 'enemies')
        self.constraintsSprites = self.createTileGroup(IMPORT_CSV(levelData['constraints']), 'constraints')

    def createTileGroup(self, layout, type):
        spriteGroup = pygame.sprite.Group()
        for rowIndex, row in enumerate(layout):
            for colIndex, ID in enumerate(row):
                if ID != '-1':
                    x = colIndex * TILE_SIZE
                    y = rowIndex * TILE_SIZE
                    if type == 'terrain':
                        terrainTileList = IMPORT_GRAPHICS('assets/world/tilesheet.png')
                        tileSurf = terrainTileList[int(ID)]
                        sprite = STATIC_TILE(TILE_SIZE, x, y, tileSurf)

                    if type == 'grass':
                        grassTileList = IMPORT_GRAPHICS('assets/world/grass.png')
                        tileSurf = grassTileList[int(ID)]
                        sprite = STATIC_TILE(TILE_SIZE, x, y, tileSurf)

                    if type == 'crates':
                        sprite = CRATE(TILE_SIZE, x, y)

                    if type == 'coins':
                        sprite = COIN(TILE_SIZE, x, y, 'assets/world/coins')

                    if type == 'FGTrees':
                        if ID == '0': sprite = TREE(TILE_SIZE, x, y, 'assets/world/smallTree', 4)
                        if ID == '1': sprite = TREE(TILE_SIZE, x, y, 'assets/world/largeTree', 12)

                    if type == 'BGTrees':
                        sprite = TREE(TILE_SIZE, x, y, 'assets/world/bgTree', 8)

                    if type == 'enemies':
                        sprite = ENEMY(TILE_SIZE, x, y)

                    if type == 'constraints':
                        sprite = TILE(TILE_SIZE, x, y)
                    spriteGroup.add(sprite)
        return spriteGroup

    def playerSetup(self, layout):
        for rowIndex, row in enumerate(layout):
            for colIndex, ID in enumerate(row):
                x = colIndex * TILE_SIZE
                y = rowIndex * TILE_SIZE
                if ID == '0':
                    sprite = PLAYER((x, y), self.displaySurf, self.createJmpPTCL)
                    self.player.add(sprite)
                if ID == '1':
                    goalSurf = pygame.image.load('assets/world/goal.png').convert_alpha()
                    sprite = STATIC_TILE(TILE_SIZE, x, y, goalSurf)
                    self.goal.add(sprite)

    def enemyCollisionReverse(self):
        for enemy in self.enemySprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraintsSprites, False):
                enemy.reverse()

    def createJmpPTCL(self, pos):
        if self.player.sprite.FR:
            pos -= pygame.math.Vector2(0, 4)
        else:
            pos += pygame.math.Vector2(0, -4)
        jumpParticleSprite = PARTICLE_EFFECT(pos,'jump')
        self.dustSprite.add(jumpParticleSprite)

    def getPlayerOnGround(self):
        if self.player.sprite.onGND:
            self.playerOnGround = True
        else:
            self.playerOnGround = False

    def createLandDust(self):
        if not self.playerOnGround and self.player.sprite.onGND and not self.dustSprite.sprites():
            if self.player.sprite.FR:
                offset = pygame.math.Vector2(0, 4)
            else:
                offset = pygame.math.Vector2(0, 4)
            fallDustParticle = PARTICLE_EFFECT(self.player.sprite.rect.midbottom - offset,'land')
            self.dustSprite.add(fallDustParticle)

    def collisions(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidableSprites = self.terrainSprites.sprites() + self.crateSprites.sprites() + self.BGTreeSprites.sprites()
        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.onL = True
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onR = True
                    self.currentX = player.rect.right
        player.applyGravity()
        self.getPlayerOnGround()
        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGND = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCLG = True
        self.hasTheMovedOff(player)

    def hasTheMovedOff(self, player):
        if player.onL and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onL = False
        if player.onR and (player.rect.right > self.currentX or player.direction.x <= 0):
            player.onR = False
        if player.onGND and player.direction.y < 0 or player.direction.y > 1:
            player.onGND = False
        if player.onCLG and player.direction.y > 0.1:
            player.onCLG = False

    def scrollX(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < ASCREEN_WIDTH / 4 and direction_x < 0:
            self.worldShift = 2
            player.speed = 0
        elif player_x > ASCREEN_WIDTH - (ASCREEN_WIDTH / 4) and direction_x > 0:
            self.worldShift = -2
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 2

    def run(self):
        self.sky.draw(self.displaySurf)
        self.clouds.draw(self.displaySurf, self.worldShift)

        self.BGTreeSprites.update(self.worldShift)
        self.BGTreeSprites.draw(self.displaySurf)

        self.terrainSprites.update(self.worldShift)
        self.terrainSprites.draw(self.displaySurf)

        self.enemySprites.update(self.worldShift)
        self.constraintsSprites.update(self.worldShift)
        self.enemyCollisionReverse()
        self.enemySprites.draw(self.displaySurf)

        self.crateSprites.update(self.worldShift)
        self.crateSprites.draw(self.displaySurf)

        self.grassSprites.update(self.worldShift)
        self.grassSprites.draw(self.displaySurf)

        self.coinSprites.update(self.worldShift)
        self.coinSprites.draw(self.displaySurf)

        self.FGTreeSprites.update(self.worldShift)
        self.FGTreeSprites.draw(self.displaySurf)

        self.dustSprite.update(self.worldShift)
        self.dustSprite.draw(self.displaySurf)

        self.player.update()
        self.collisions()
        self.createLandDust()
        self.scrollX()
        self.player.draw(self.displaySurf)
        self.goal.update(self.worldShift)
        self.goal.draw(self.displaySurf)

        self.water.draw(self.displaySurf, self.worldShift)
