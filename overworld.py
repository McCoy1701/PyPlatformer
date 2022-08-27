import pygame
from gameData import *
from support import IMPORT_FOLDER

class NODE(pygame.sprite.Sprite):
    def __init__(self, pos, status, iconSpeed, path):
        super().__init__()
        self.frames = IMPORT_FOLDER(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        if status == 'Available':
            self.status = 'Available'
        else:
            self.status = 'Locked'

        self.rect = self.image.get_rect(center = pos)
        self.detectionZone = pygame.Rect(self.rect.centerx - (iconSpeed / 2), self.rect.centery - (iconSpeed / 2), iconSpeed, iconSpeed)

    def animate(self):
        self.frameIndex += 0.15
        if self.frameIndex >= len(self.frames): self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def update(self):
        if self.status == 'Available':
            self.animate()
        else:
            tintSurf = self.image.copy()
            tintSurf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tintSurf, (0,0))


class ICON(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.importAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.status = 'idle'
        self.FR = True
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(center = pos)

    def importAssets(self):
        characterPath = 'assets/'
        self.animations = {'idle':[],'run':[]}

        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = IMPORT_FOLDER(fullPath)

    def iconAnimate(self):
        animation = self.animations[self.status]

        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        image = animation[int(self.frameIndex)]
        self.image = image

    def update(self):
        self.iconAnimate()
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
                nodeSprite = NODE(nodeData['nodePos'], 'Available', self.speed, nodeData['nodeGraphics'])
            else:
                nodeSprite = NODE(nodeData['nodePos'], 'Locked', self.speed, nodeData['nodeGraphics'])
            self.nodes.add(nodeSprite)

    def setupIcon(self):
        self.icon = pygame.sprite.GroupSingle()
        iconSprite = ICON(self.nodes.sprites()[self.currentLevel].rect.center)
        self.icon.add(iconSprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT] and self.currentLevel < self.maxLevel or keys[pygame.K_d] and self.currentLevel < self.maxLevel:
                self.moveDirection = self.getMovement('next')
                self.currentLevel += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.currentLevel > 0 or keys[pygame.K_a] and self.currentLevel > 0:
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
        pygame.draw.lines(self.displaySurf, 'purple', False, points, 2)

    def run(self):
        self.input()
        self.updateIconPos()
        self.icon.update()
        self.nodes.update()
        if self.maxLevel != 0:
            self.drawPath()
        self.nodes.draw(self.displaySurf)
        self.icon.draw(self.displaySurf)
