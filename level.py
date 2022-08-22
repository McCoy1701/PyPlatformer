import pygame
from tiles import TILE, STATIC_TILE, CRATE, COIN, TREE
from support import IMPORT_CSV, IMPORT_GRAPHICS
from enemy import ENEMY
from settings import *

class LEVEL:
    def __init__(self, levelData, surf):
        
        self.worldShift = 0
        self.displaySurf = surf #Assings displaySurf to passed arg surf
        
        #LevelSetup
        terrainLayout = IMPORT_CSV(levelData['terrain'])
        self.terrainSprites = self.createTileGroup(terrainLayout, 'terrain')
        
        #Grass
        grassLayout = IMPORT_CSV(levelData['grass'])
        self.grassSprites = self.createTileGroup(grassLayout, 'grass')
        
        #Crates
        crateLayout = IMPORT_CSV(levelData['crates'])
        self.crateSprites = self.createTileGroup(crateLayout, 'crates')
        
        #Coins
        coinLayout = IMPORT_CSV(levelData['coins'])
        self.coinSprites = self.createTileGroup(coinLayout, 'coins')
        
        #foreground Trees
        FGTreeLayout = IMPORT_CSV(levelData['FGTrees'])
        self.FGTreeSprites = self.createTileGroup(FGTreeLayout, 'FGTrees')
        
        BGTreeLayout = IMPORT_CSV(levelData['BGTrees'])
        self.BGTreeSprites = self.createTileGroup(BGTreeLayout, 'BGTrees')
        
        enemyLayout = IMPORT_CSV(levelData['enemies'])
        self.enemySprites = self.createTileGroup(enemyLayout, 'enemies')
        
        constraintsLayout = IMPORT_CSV(levelData['constraints'])
        self.constraintsSprites = self.createTileGroup(constraintsLayout, 'constraints')

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

    def enemyCollisionReverse(self):
        for enemy in self.enemySprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraintsSprites, False):
                enemy.reverse()
    
    def run(self):
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
        
        
