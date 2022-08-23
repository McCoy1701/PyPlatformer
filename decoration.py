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
        waterStart = -SCREEN_WIDTH
        waterTileW = 24
        tileAmount = int((lvlWidth + SCREEN_WIDTH * 2) / waterTileW)
        self.waterSprites = pygame.sprite.Group()
        for tile in range(tileAmount):
            x = tile * waterTileW + waterStart
            y = top
            sprite = ANIMATED_TILE(waterTileW, x, y, 'assets/world/water')
            self.waterSprites.add(sprite)
    
    def draw(self, surf, shift):
        self.waterSprites.update(shift)
        self.waterSprites.draw(surf)

class CLOUD:
    def __init__(self, horizon, lvlWidth, cloudNum):
        cloudSurf = IMPORT_FOLDER('assets/world/clouds')
        minX = -SCREEN_WIDTH
        maxX = lvlWidth + SCREEN_WIDTH
        minY = 0
        maxY = horizon
        self.cloudSprites = pygame.sprite.Group()
        
        for cloud in range(cloudNum):
            cloud = choice(cloudSurf)
            x = randint(minX, maxX)
            y = randint(minY, maxY)
            sprite = STATIC_TILE(0, x, y, cloud)
            self.cloudSprites.add(sprite)
    
    def draw(self, surf, shift):
        self.cloudSprites.update(shift)
        self.cloudSprites.draw(surf)