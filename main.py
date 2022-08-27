import pygame, sys
from settings import *
from level import LEVEL
from gameData import *
from overworld import OVERWORLD
from debug import debug

class GAME:
    def __init__(self):
        self.maxLevel = 2
        self.status = 'overworld'
        self.overworld = OVERWORLD(0, self.maxLevel, display, self.createLevel)

    def createOverworld(self, currentLevel, newMaxLevel):
        if newMaxLevel > self.maxLevel:
            self.maxLevel = newMaxLevel
        self.overworld = OVERWORLD(currentLevel, self.maxLevel, display, self.createLevel)
        self.status = 'overworld'

    def createLevel(self, currentLevel):
        self.level = LEVEL(currentLevel, display, self.createOverworld)
        self.status = 'level'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
display = pygame.Surface((ASCREEN_WIDTH, ASCREEN_HEIGHT))
clock = pygame.time.Clock()
Active = True
game = GAME()

pygame.display.set_caption('PyPlatformer')

while Active:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    display.fill('white')
    game.run()

    surf = pygame.transform.scale(display, (SCREEN_HEIGHT, SCREEN_WIDTH))
    screen.blit(surf, (0, 0))

    debug(clock)
    pygame.display.update()
