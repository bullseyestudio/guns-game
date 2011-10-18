import constants
import battle
import gui

import pygame
from pygame.locals import *

class Bullet:

	def __init__( self, pos ):
		self.position = pos
		self.size = 1
		self.timer = 0
		self.sizechange = 1

	def redraw( self, screen ):
		global all

		selfpos = ( int( self.position[0] * gui.zoom) , int( self.position[1] * gui.zoom ) )
		plrpos = ( int( battle.cplr.position[0] * gui.zoom) , int( battle.cplr.position[1] * gui.zoom ) )

		self.timer += 1

		if self.timer > 10:
			self.sizechange = -1

		if self.timer > 20:
			all.remove(self)

		if self.size > 0:
			srf = pygame.Surface( ( self.size * 2, self.size * 2 ) )

			opos = [ selfpos[0] - plrpos[0] +  ( gui.screen.get_width() /2 ), selfpos[1] - plrpos[1] +  ( gui.screen.get_height() /2 ) ]
			pos = [a - b for a, b in zip(opos, (self.size, self.size))]

			pygame.draw.rect( srf, ( 0, 0, 0 ), srf.get_rect() )
			gui.screen.blit( srf, pos )

			self.size = self.size + self.sizechange


all = []
