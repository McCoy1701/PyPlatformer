import pygame
from settings import *
from tiles import ANIMATED_TILE, STATIC_TILE
from support import IMPORT_FOLDER
from random import choice, randint

class SKY:
    def __init__(self, horizon):
        self.top = pygame.image.load('assets/world/sky/skyTop.png').convert()
        self.middle = pygame.image.load('assets/world/sky/skyMiddle.png').convert()
        self.bottom = pygame.image.load('assets/world/sky/skyBottom.png').convert()
        self.horizon = horizon
        
        self.top = pygame.transform.scale(self.top, (ASCREEN_WIDTH, TILE_SIZE))
        self.middle = pygame.transform.scale(self.middle, (ASCREEN_WIDTH, TILE_SIZE))
        self.bottom = pygame.transform.scale(self.bottom, (ASCREEN_WIDTH, TILE_SIZE))
        
    def draw(self, surf):
        for row in range(verticalTile):
            y = row * TILE_SIZE
            if row < self.horizon:
                surf.blit(self.top, (0, y))
            elif row == self.horizon:
                surf.blit(self.middle, (0, y))
            else:
                surf.blit(self.bottom, (0, y))

class WATER:
    def __init__(self, top, lvlWidth):
        self.waterStart = -SCREEN_WIDTH
        self.waterTileW = 24
        self.top = top
        self.tileAmount = int((lvlWidth + SCREEN_WIDTH * 2) / self.waterTileW)
        self.generateWaterTiles()

    def generateWaterTiles(self):
        self.waterSprites = pygame.sprite.Group()
        for tile in range(self.tileAmount):
            x = tile * self.waterTileW + self.waterStart
            y = self.top
            sprite = ANIMATED_TILE(self.waterTileW, x, y, 'assets/world/water')
            self.waterSprites.add(sprite)

    def draw(self, surf, shift):
        self.waterSprites.update(shift)
        self.waterSprites.draw(surf)

class CLOUD:
    def __init__(self, horizon, lvlWidth, cloudNum):
        self.cloudSurf = IMPORT_FOLDER('assets/world/clouds')
        self.minX = -SCREEN_WIDTH
        self.maxX = lvlWidth + SCREEN_WIDTH
        self.cloudNum = cloudNum
        self.minY = 0
        self.maxY = horizon
        self.generateClouds()

    def generateClouds(self):
        self.cloudSprites = pygame.sprite.Group()
        for cloud in range(self.cloudNum):
            cloud = choice(self.cloudSurf)
            x = randint(self.minX, self.maxX)
            y = randint(self.minY, self.maxY)
            sprite = STATIC_TILE(0, x, y, cloud)
            self.cloudSprites.add(sprite)
    
    def draw(self, surf, shift):
        self.cloudSprites.update(shift)
        self.cloudSprites.draw(surf)