import pygame
from support import importFolder

class PLAYER(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.importAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        
        #DUST
        self.importDust()
        self.dustIndex = 0
        self.dustSpeed = 0.15
        self.displaySurface = surface
        
        #PLAYER MOVEMENT
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 1
        self.gravity = 0.8
        self.jumpSpeed = -10

        self.status = 'idle'
        self.FR = True #Facing Right
        self.onGND = False #on Ground
        self.onCLG = False #on Ceiling
        self.onL = False #on Left
        self.onR = False #on Right

    def importAssets(self):
        characterPath = 'assets/' #Local var assinged to the assets folder
        self.animations = {'idle': [], 'run': [], 'jump':[], 'fall':[]} #dictionary of animations

        for animation in self.animations.keys(): #Gets each key in the animations dictionary
            fullPath = characterPath + animation #Assings local var to assets animation path
            self.animations[animation] = importFolder(fullPath) #Assings the animations key to the images in the folder

    def importDust(self):
        self.dustRun = importFolder('assets/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status] #Get the animation
        self.frameIndex += self.animationSpeed #increase the frameIndex with animationSpeed
        if self.frameIndex >= len(animation): self.frameIndex = 0 # if the frameIndex is greater than or equal to the length of the animation set frameIndex to 0

        img = animation[int(self.frameIndex)] #Assign img to animation with the frameIndex as the key
        if self.FR: #If Facing Right
            self.image = img #Assign self.image to current frame
        else: #If not Facing Right(facing left)
            flipped = pygame.transform.flip(img, True, False) #Flip image
            self.image = flipped #Assign image to the new flipped image

        if self.onGND and self.onR: 
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.onGND and self.onL:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.onGND:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        elif self.onCLG and self.onR:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.onCLG and self.onL:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.onCLG:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 2
            self.Right = True
            self.FR = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -2
            self.Right = False
            self.FR = False  
        elif keys[pygame.K_SPACE] and self.onGND:
            self.jump()
        else:
            self.direction.x = 0

    def getStatus(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jumpSpeed

    def update(self):
        self.playerInput()
        self.getStatus()
        self.animate()
