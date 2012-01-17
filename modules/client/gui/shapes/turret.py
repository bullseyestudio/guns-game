import pygame, math
from modules.client.gui.shapes import bullet

class Turret(object):
	""" A turret is basically a circle with a triangle inside showing its front """

	def __init__(self, surface, position):
		self.surface = surface
		self.pos = position
		self.dot_pos = None
		self.last_shot_time = 0

		self.box = pygame.Surface((64, 64), 0, self.surface)
		self.box.fill((255,0,255))
		self.box.set_colorkey((255,0,255))
		pygame.draw.circle(self.box, (255,255,255), (32,32), 30)
		pygame.draw.circle(self.box, (0,0,0), (32,32), 30, 2)

	def point_at(self, position):
		self.target = position

		if self.dot_pos:
			pygame.draw.circle(self.box, (255,255,255), self.dot_pos, 2, 0)

		rel_pos = [b - a for a, b in zip(self.pos, position)]
		dist = math.hypot(*rel_pos)
		ratio = 26 / dist

		new_pos = [int(a * ratio) + 32 for a in rel_pos]

		pygame.draw.circle(self.box, (0,0,0), new_pos, 2, 0)
		self.dot_pos = new_pos
		pass

	def paint(self):
		dest_pos = self.box.get_rect()
		dest_pos.center = self.pos

		self.surface.blit(self.box, dest_pos)

		return dest_pos

	def fire(self):
		now = pygame.time.get_ticks()

		diff = abs(now - self.last_shot_time)

		if(diff > 100):
			bpos = [a + (b - 32) for a,b in zip(self.pos, self.dot_pos)]
			bspd = [int((a - 32) / 4) for a in self.dot_pos]

			rel_pos = [b - a for a, b in zip(self.pos, self.target)]
			dist = math.hypot(*rel_pos) - 28

			bullet.new(bpos, bspd, dist, 0, 0)

			self.last_shot_time = now
