import pygame, math
from modules.client.gui import common

# Flags for bullets:
TRACKING = 1
LASER = 2
# The above are mutually exclusive; if ORed together, LASER wins

class Bullet(object):
	def __init__(self, position, speed, distance, inertia, flags = 0):
		self.initial_position = position
		self.position = position
		self.speed = speed
		self.distance = distance
		self.inertia = inertia
		self.flags = flags
		self.exploding = False
		self.last_think_time = 0
		self.surface = pygame.Surface((16, 16))
		self.surface.fill((255, 0, 255))
		self.surface.set_colorkey((255, 0, 255))
		pygame.draw.circle(self.surface, (0,0,0), (5,5), 3)

		if self.flags & (LASER | TRACKING):
			self.flags = self.flags & (~TRACKING)

	def think(self):
		now = pygame.time.get_ticks()

		diff = abs(now - self.last_think_time)

		if(diff < 50):
			return

		self.last_think_time = now

		if self.exploding:
			return self.think_explode()

		self.position = [a + b for a,b in zip(self.position, self.speed)]

		if self.flags & TRACKING:
			pass # TODO: Adjust speed to curve towards cursor.
		elif self.flags & LASER:
			pass # TODO: Make a line. Make it go straight to the target.

		xdist = self.position[0] - self.initial_position[0]
		ydist = self.position[1] - self.initial_position[1]

		distance = math.sqrt(xdist ** 2 + ydist ** 2)

		if distance >= self.distance:
			self.exploding = True

	def think_explode(self):
		all.remove(self)

	def render(self):
		if self.exploding:
			return # TODO: Make boomies (again)

		if self.flags & LASER:
			pass # TODO: Make pretty line

		common.screen.blit(self.surface, self._rect())

	def unrender(self):
		if self.exploding:
			return # TODO: Make boomies (again)

		if self.flags & LASER:
			pass # TODO: Make pretty line

		common.draw_background_rect(self._rect())

	def _rect(self):
		""" Returns a pygame.Rect for the bullet's onscreen position """
		rect = pygame.Rect(0,0, 16,16)
		rect.center = self.position

		return rect

all = []

def new(position, speed, distance, inertia, flags):
	bullet = Bullet(position, speed, distance, inertia, flags)

	all.append(bullet)

	return bullet
