from modules.client import constants, battle, gui

import pygame
from pygame.locals import *

class Bullet:

	def __init__( self, pos ):
		self.position = pos
		self.size = 1
		self.timer = 0
		self.sizechange = 1

	def redraw( self ):
		global all

		self.timer += 1

		if self.timer > 10:
			self.sizechange = -1

		if self.timer > 20:
			all.remove(self)

		if self.size > 0:
			srf = pygame.Surface( ( self.size * 2, self.size * 2 ) )

			opos = gui.map_to_screen(self.position)
			pos = [a - b for a, b in zip(opos, (self.size, self.size))]

			pygame.draw.rect( srf, ( 0, 0, 0 ), srf.get_rect() )
			gui.screen.blit( srf, pos )

			self.size = self.size + self.sizechange


all = []
