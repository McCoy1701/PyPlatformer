import pygame
from csv import reader
from os import walk
from settings import TILE_SIZE

def IMPORT_FOLDER(path):
    surfaceList = []
    for _, __, info in walk(path):
        for img in info:
            fullPath = path + '/' + img
            infoSurf = pygame.image.load(fullPath).convert_alpha()
            surfaceList.append(infoSurf)
    return surfaceList

def IMPORT_CSV(path):
    terrainMap = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrainMap.append(list(row))
        return terrainMap

def IMPORT_GRAPHICS(path):
    surface = pygame.image.load(path).convert_alpha()
    tileNumX = int(surface.get_size()[0] / TILE_SIZE)
    tileNumY = int(surface.get_size()[1] / TILE_SIZE)
    cutTiles = []
    for row in range(tileNumY):
        for col in range(tileNumX):
            X = col * TILE_SIZE
            Y = row * TILE_SIZE
            new_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), flags= pygame.SRCALPHA)
            new_surf.blit(surface,(0,0),pygame.Rect(X, Y, TILE_SIZE, TILE_SIZE))
            cutTiles.append(new_surf)
    return cutTiles
