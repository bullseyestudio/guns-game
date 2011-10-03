
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

class Player:

	def __init__(self, newname):
		self.name = newname
		self.position = [ 0, 0 ]
		self.textcolor = ( 10, 10, 10 )
		self.tankshape = [0,0,48,64]
		self.srf = pygame.Surface( ( self.tankshape[2], self.tankshape[3] ) ) # global_.font.render( self.name, 1, self.textcolor )
		self.srf.fill( ( 255, 0, 255 ) )
		self.srf.set_colorkey( ( 255, 0, 255 ) )
#		self.textpos = self.text.get_rect()
		pygame.draw.rect( self.srf, self.textcolor, self.tankshape, 3 )
		pygame.draw.rect( self.srf, self.textcolor, ( ( self.tankshape[2] / 2 ) - 5, 5, 10, 10 ), 3 )
		self.rotation = float( 0.0 )
		

	def redraw(self, screen):
#		global_.screen.blit( global_.background, self.textpos, self.tankshape)
#		global_.screen.blit( global_.background, self.textpos, self.textpos)
		
		srf2 = pygame.transform.rotate( self.srf, self.rotation )
		srf = global_.font.render( self.name, 1, self.textcolor )
		
		srect = srf.get_rect()
		srect2 = srf2.get_rect()
		
		srect.centerx = self.tankshape[2] / 2
		srect.centery = self.tankshape[2] / 3
		
		global_.screen.blit( srf, ( self.position[0] + ( ( srect2.width - srect.width ) / 2 ), self.position[1] - 15 ) )
		
#		global_.screen.blit( tank_shapes, self.textpos, self.tankshape )
		global_.screen.blit( srf2, ( self.position[0], self.position[1] ) )

global_.players = {}
global_.cid = 0
