import constants

import pygame
from pygame.locals import *

class Bullet:

	def __init__( self, pos ):
		self.position = pos
		self.size = 1
		self.timer = 0
		self.sizechange = 1

	def redraw( self, screen ):
		selfpos = ( int( self.position[0] * constants.zoom) , int( self.position[1] * constants.zoom ) )
		plrpos = ( int( constants.cplr.position[0] * constants.zoom) , int( constants.cplr.position[1] * constants.zoom ) )
		if self.size > 0:
			srf = pygame.Surface( ( self.size * 2, self.size * 2 ) )
			#opos = [ self.position[0] - constants.cplr.position[0] + ( constants.screen.get_width() /2 ), self.position[1] - constants.cplr.position[1] + ( constants.screen.get_height() /2 ) ]
			opos = [ selfpos[0] - plrpos[0] +  ( constants.screen.get_width() /2 ), selfpos[1] - plrpos[1] +  ( constants.screen.get_height() /2 ) ]
			pos = [a - b for a, b in zip(opos, (self.size, self.size))]

			pygame.draw.rect( srf, ( 0, 0, 0 ), srf.get_rect() )
			constants.screen.blit( srf, pos )

			if self.timer > 10:
				self.size = self.size + self.sizechange
				self.timer = 0

				if self.size > 10:
					self.sizechange = -1

			self.timer = self.timer + 1

all = []
