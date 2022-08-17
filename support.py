import pygame
from os import walk

def importFolder(path):
    SurfaceList = [] #List of Surfaces
    for _, __, imgFiles in walk(path): #Get the Images from the folder
        for img in imgFiles: #Parse the images
            fullPath = path + '/' + img #Local var set to the image path
            surf = pygame.image.load(fullPath).convert_alpha() #Load the image using pygame.image.load
            SurfaceList.append(surf) #Place the surf in SurfaceList
    return SurfaceList