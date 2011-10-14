
import sys

sys.path.append('./modules')
sys.path.append('../common/modules')

import global_

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

class Bullet:
	
	def __init__( self, pos ):
		self.position = pos
		self.size = 1
		self.timer = 0
		self.sizechange = 1
	
	def redraw( self, screen ):
		selfpos = ( int( self.position[0] * global_.zoom) , int( self.position[1] * global_.zoom ) )
		plrpos = ( int( global_.cplr.position[0] * global_.zoom) , int( global_.cplr.position[1] * global_.zoom ) )
		if self.size > 0:
			srf = pygame.Surface( ( self.size * 2, self.size * 2 ) )
			#opos = [ self.position[0] - global_.cplr.position[0] + ( global_.screen.get_width() /2 ), self.position[1] - global_.cplr.position[1] + ( global_.screen.get_height() /2 ) ]
			opos = [ selfpos[0] - plrpos[0] +  ( global_.screen.get_width() /2 ), selfpos[1] - plrpos[1] +  ( global_.screen.get_height() /2 ) ]
			pos = [a - b for a, b in zip(opos, (self.size, self.size))]
			
			pygame.draw.rect( srf, ( 0, 0, 0 ), srf.get_rect() )
			global_.screen.blit( srf, pos )
			
			if self.timer > 10:
				self.size = self.size + self.sizechange
				self.timer = 0
				
				if self.size > 10:
					self.sizechange = -1
			
			self.timer = self.timer + 1
