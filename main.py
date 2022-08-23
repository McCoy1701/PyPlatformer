import pygame, sys
from settings import *
from level import LEVEL
from gameData import *
from debug import debug

pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
display = pygame.Surface((ASCREEN_WIDTH, ASCREEN_HEIGHT))
clock = pygame.time.Clock()
Active = True
level = LEVEL(level0, display)

pygame.display.set_caption('PyPlatformer')

while Active:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    display.fill('black')
    level.run()

    surf = pygame.transform.scale(display, (SCREEN_HEIGHT, SCREEN_WIDTH))
    screen.blit(surf, (0, 0))

    debug(clock)
    pygame.display.update()
