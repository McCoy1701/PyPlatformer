import pygame 
from support import IMPORT_FOLDER

class PLAYER(pygame.sprite.Sprite):
	def __init__(self, pos, surface, createJmpPTCL):
		super().__init__()
		self.importAssets()
		self.frameIndex = 0
		self.animationSpeed = 0.15
		self.image = self.animations['idle'][self.frameIndex]
		self.rect = self.image.get_rect(topleft = pos)

		self.importDustParticles()
		self.dustFrame = 0
		self.dustSpeed = 0.15
		self.displaySurf = surface
		self.createJmpPTCL = createJmpPTCL

		self.direction = pygame.math.Vector2(0,0)
		self.speed = 1
		self.gravity = 0.8
		self.jumpSpeed = -8

		self.status = 'idle'
		self.FR = True
		self.onGND = False
		self.onCLG = False
		self.onL = False
		self.onR = False

	def importAssets(self):
		characterPath = 'assets/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			fullPath = characterPath + animation
			self.animations[animation] = IMPORT_FOLDER(fullPath)

	def importDustParticles(self):
		self.dustRun = IMPORT_FOLDER('assets/dust_particles/run')

	def animate(self):
		animation = self.animations[self.status]

		self.frameIndex += self.animationSpeed
		if self.frameIndex >= len(animation):
			self.frameIndex = 0

		image = animation[int(self.frameIndex)]
		if self.FR:
			self.image = image
		else:
			flipped = pygame.transform.flip(image,True,False)
			self.image = flipped

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

	def runDustAnimation(self):
		if self.status == 'run' and self.onGND:
			self.dustFrame += self.dustSpeed
			if self.dustFrame >= len(self.dustRun):
				self.dustFrame = 0

			dustParticle = self.dustRun[int(self.dustFrame)]

			if self.FR:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.displaySurf.blit(dustParticle, pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flippedDust = pygame.transform.flip(dustParticle,True,False)
				self.displaySurf.blit(flippedDust, pos)

	def getInput(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT] or keys[pygame.K_a]:
			self.direction.x = -2
			self.FR = False
		elif keys[pygame.K_LEFT] or keys[pygame.K_d]:
			self.direction.x = 2
			self.FR = True
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.onGND:
			self.jump()
			self.createJmpPTCL(self.rect.midbottom)

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
		self.getInput()
		self.getStatus()
		self.animate()
		self.runDustAnimation()
