import pygame 
from settings import *
from support import IMPORT_FOLDER

class TILE(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))
    
    def update(self, shift):
        self.rect.x += shift

class STATIC_TILE(TILE):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class CRATE(STATIC_TILE):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('assets/world/crate.png').convert_alpha())
        offsetY = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offsetY))

class ANIMATED_TILE(TILE):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = IMPORT_FOLDER(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
    
    def animate(self):
        self.frameIndex += 0.15
        if self.frameIndex >= len(self.frames): self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]
    
    def update(self, shift):
        self.animate()
        self.rect.x += shift

class COIN(ANIMATED_TILE):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        centerX = x + int(size/2)
        centerY = y + int(size/2)
        self.rect = self.image.get_rect(center = (centerX, centerY))

class TREE(ANIMATED_TILE):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offsetY = y - offset
        self.rect.topleft = (x, offsetY)
