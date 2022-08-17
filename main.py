import pygame, sys
from settings import *
from level import *
from debug import debug

pygame.init() #Initalize pygame
Active = True #Sets the main gameLoop active
clock = pygame.time.Clock() #clock for pygame
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH)) #Set the size of the main screen
display = pygame.Surface((ASCREEN_WIDTH, ASCREEN_HEIGHT)) #Set the size of the display screen
level = LEVEL(gameMap, display) #Instance LEVEL
pygame.display.set_caption('PyPlatformer') #Set the caption of the window

while Active: #Main GameLoop
    display.fill('cyan') #Fill the display with White
    clock.tick(fps) #Set the clock to 60 fps
    for event in pygame.event.get(): #Listen for events
        if event.type == pygame.QUIT: #Quit if the event.type is pygame.QUIT
            pygame.quit() #quit
            sys.exit() #exit

    level.run() #Starts executing code in the run method of LEVEL

    surf = pygame.transform.scale(display, (SCREEN_HEIGHT, SCREEN_WIDTH)) #local var surf scales display to SCREEN_WIDTH/HEIGHT in setting
    screen.blit(surf, (0, 0)) #block bit transfer local var surf to screen

    debug(clock) #Executes the debugger
    pygame.display.update() #Update a portion of the screen
