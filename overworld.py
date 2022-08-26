import pygame
from gameData import *

class NODE(pygame.sprite.Sprite):
    def __init__(self, pos, status, iconSpeed):
        super().__init__()
        self.image = pygame.Surface((16, 12))
        self.rect = self.image.get_rect(center = pos)
        if status == 'Available':
            self.image.fill('red')
        else:
            self.image.fill('gray')
        self.detectionZone = pygame.Rect(self.rect.centerx - (iconSpeed / 2), self.rect.centery - (iconSpeed / 2), iconSpeed, iconSpeed)

class ICON(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((8, 8))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos

class OVERWORLD:
    def __init__(self, startLevel, maxLevel, surf, createLevel):
        self.displaySurf = surf
        self.maxLevel = maxLevel
        self.currentLevel = startLevel
        self.createLevel = createLevel

        self.moving = False
        self.moveDirection = pygame.math.Vector2(0,0)
        self.speed = 2

        self.setupNodes()
        self.setupIcon()

    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        for nodeIndex, nodeData in enumerate(levels.values()):
            if nodeIndex <= self.maxLevel:
                nodeSprite = NODE(nodeData['nodePos'], 'Available', self.speed)
            else:
                nodeSprite = NODE(nodeData['nodePos'], 'Locked', self.speed)
            self.nodes.add(nodeSprite)

    def setupIcon(self):
        self.icon = pygame.sprite.GroupSingle()
        iconSprite = ICON(self.nodes.sprites()[self.currentLevel].rect.center)
        self.icon.add(iconSprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.currentLevel < self.maxLevel:
                self.moveDirection = self.getMovement('next')
                self.currentLevel += 1
                self.moving = True
            elif keys[pygame.K_LEFT] or keys[pygame.K_a] and self.currentLevel > 0:
                self.moveDirection = self.getMovement('pee')
                self.currentLevel -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.createLevel(self.currentLevel)

    def getMovement(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel - 1].rect.center)

        return (end - start).normalize()

    def updateIconPos(self):
        if self.moving and self.moveDirection:
            self.icon.sprite.pos += self.moveDirection * self.speed
            targetNode = self.nodes.sprites()[self.currentLevel]
            if targetNode.detectionZone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.moveDirection = pygame.math.Vector2(0, 0)

    def drawPath(self):
        points = [node['nodePos'] for index, node in enumerate(levels.values()) if index <= self.maxLevel]
        pygame.draw.lines(self.displaySurf, 'purple', False, points, 1)

    def run(self):
        self.input()
        self.updateIconPos()
        self.icon.update()
        if self.maxLevel != 0:
            self.drawPath()
        self.nodes.draw(self.displaySurf)
        self.icon.draw(self.displaySurf)
