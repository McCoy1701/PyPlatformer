import pygame

pygame.init()
FONT = pygame.font.Font('font/Pixeltype.ttf', 16)

def debug(text, x = 60, y = 20):
    DISPLAY = pygame.display.get_surface()
    debugSF = FONT.render(str(text), False, 'black')
    debugRect = debugSF.get_rect(center = (x, y))
    DISPLAY.blit(debugSF, debugRect)