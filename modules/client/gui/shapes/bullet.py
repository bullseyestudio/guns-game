import pygame, math

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
		pass # TODO: make boomies

	def render(self):
		if self.exploding:
			pass # TODO: Make boomies (again)

		if self.flags & LASER:
			pass # TODO: Make pretty line

		# TODO: Render thine self!

	def _rect(self):
		pass # TODO: Return a pygame.Rect() of the bullet's current position.

all = []
