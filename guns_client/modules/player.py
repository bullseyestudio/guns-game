
import sys

sys.path.append('./modules')
sys.path.append('../common/modules')

import global_
from global_ import *

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
		self.text = global_.font.render( self.name, 1, self.textcolor )
		self.textpos = self.text.get_rect()
		self.tankshape = [0,0,64,48]

	def redraw(self, screen):
#		global_.screen.blit( global_.background, self.textpos, self.tankshape)
#		global_.screen.blit( global_.background, self.textpos, self.textpos)

		self.textpos.centerx = self.position[0]
		self.textpos.centery = self.position[1]

#		global_.screen.blit( tank_shapes, self.textpos, self.tankshape )
		global_.screen.blit( self.text, self.textpos )

global_.players = {}
global_.cid = 0