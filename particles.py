import pygame
from support import IMPORT_FOLDER

class PARTICLE_EFFECT(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frameIndex = 0
        self.animationSpeed = .5
        self.checkType(type)
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect(center = pos)
    
    def checkType(self, type):
        if type == 'jump':
            self.frames = IMPORT_FOLDER('assets/dust_particles/jump')
        if type == 'land':
            self.frames = IMPORT_FOLDER('assets/dust_particles/land')
    
    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frameIndex)]

    def update(self, xShift):
        self.animate()
        self.rect.x += xShift
