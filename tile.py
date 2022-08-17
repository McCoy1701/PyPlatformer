from tkinter import Toplevel
import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, type, pos, size):
        super().__init__()
        self.type = type
        self.size = size
        self.grass = pygame.image.load('assets/world/grass.png').convert_alpha()
        self.dirt = pygame.image.load('assets/world/dirt.png').convert_alpha()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)
        if self.type == 2:
            self.image= self.grass
        elif self.type == 1:
            self.image = self.dirt
    
    def update(self, xShift):
        self.rect.x += xShift
