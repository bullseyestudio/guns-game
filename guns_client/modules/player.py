
import sys
import math

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
		self.view_offset = { 'top':10, 'left':58, 'bottom':74, 'right':10}
		self.srf = pygame.Surface( ( self.tankshape[2], self.tankshape[3] ) ) # global_.font.render( self.name, 1, self.textcolor )
		self.srf.fill( ( 255, 0, 255 ) )
		self.srf.set_colorkey( ( 255, 0, 255 ) )
#		self.textpos = self.text.get_rect()
		pygame.draw.rect( self.srf, self.textcolor, self.tankshape, 3 )
		pygame.draw.rect( self.srf, self.textcolor, ( ( self.tankshape[2] / 2 ) - 5, 5, 10, 10 ), 3 )
		self.rotation = 0.0
		self.aimang = 0.0
		self.draw = True
		if(self.name == global_.username):
			global_.cplr = self
		

	def redraw(self, screen):
#		global_.screen.blit( global_.background, self.textpos, self.tankshape)
#		global_.screen.blit( global_.background, self.textpos, self.textpos)
		
		if self.draw == True:
			srf2 = pygame.transform.scale( self.srf, ( int( self.tankshape[2] * global_.zoom ), int( self.tankshape[3] * global_.zoom ) ) )
			srf2 = pygame.transform.rotate( srf2, self.rotation )
			
			srf = global_.font.render( self.name, 1, self.textcolor )
			
			srect = srf.get_rect()
			srect2 = srf2.get_rect()
			
			srect.centerx = self.tankshape[2] / 2
			srect.centery = self.tankshape[2] / 3
			
			selfpos = ( int( self.position[0] * global_.zoom) , int( self.position[1] * global_.zoom ) )
			plrpos = ( int( global_.cplr.position[0] * global_.zoom) , int( global_.cplr.position[1] * global_.zoom ) )
			
			if(global_.username == self.name):
				crdx = global_.font.render( "x:{0}".format(self.position[0]), 1, self.textcolor )
				crdy = global_.font.render( "y:{0}".format(self.position[1]), 1, self.textcolor )
				
				crectx = crdx.get_rect()
				crecty = crdy.get_rect()
				
	#			global_.screen.blit( srf, ( self.position[0] + ( ( srect2.width - srect.width ) / 2 ), self.position[1] - 15 ) )
				global_.screen.blit( srf, ( global_.screen.get_width() / 2, global_.screen.get_height() /2 - 15 ) )
				
	#			global_.screen.blit( tank_shapes, self.textpos, self.tankshape )
	#			global_.screen.blit( srf2, ( self.position[0], self.position[1] ) )
				global_.screen.blit( srf2, ( global_.screen.get_width() / 2, global_.screen.get_height() /2 ) )
		        
				global_.screen.blit( crdx, ( 5, 5 ) )
				global_.screen.blit( crdy, ( 5, crectx.height+5 ) )
			else:
				
				max_view_radius = [ ( int( screen.get_width() ) / float(global_.zoom) ) / 2,  ( int( screen.get_height() ) / float(global_.zoom) ) / 2 ]
				
				# Same long-ass check as was used first in guns_server/modules/battle.py modified to work with client variables
				if self.position[0] < ( global_.cplr.position[0] + max_view_radius[0] + self.view_offset['right'] ) and self.position[0] > ( global_.cplr.position[0] - max_view_radius[0] - self.view_offset['left'] ) and self.position[1] < ( global_.cplr.position[1] + max_view_radius[1] + self.view_offset['top'] ) and self.position[1] > ( global_.cplr.position[1] - max_view_radius[1] - self.view_offset['bottom'] ):
					offsetx = selfpos[0] - plrpos[0]
					offsety = selfpos[1] - plrpos[1]
					global_.screen.blit( srf, ( global_.screen.get_width() / 2 + offsetx, global_.screen.get_height() /2 - 15 + offsety ) )
					global_.screen.blit( srf2, ( global_.screen.get_width() / 2 + offsetx, global_.screen.get_height() /2 + offsety ) )
				else:
					# direction indicator...let's see how I do this
					
					screen_edge = {
						'left': 0,
						'right': screen.get_width() - 10,
						'top': 0,
						'bottom': screen.get_height() - 10
						}
					
					offsetx = selfpos[0] - plrpos[0]
					offsety = selfpos[1] - plrpos[1]
					origin = [ global_.screen.get_width() / 2 + offsetx, global_.screen.get_height() /2 - 15 + offsety ]
					
					srf = global_.font.render( self.name, 1, self.textcolor )
					
					toffset = [ 0, 0 ]
					
					if origin[0] < screen_edge['left']:
						origin[0] = screen_edge['left']
						toffset[0] = 10
					if origin[0] > screen_edge['right']:
						origin[0] = screen_edge['right']
						toffset[0] = ( srf.get_width() + 10 ) * -1
					
					if origin[1] < screen_edge['top']:
						origin[1] = screen_edge['top']
						toffset[1] = 10
					if origin[1] > screen_edge['bottom']:
						origin[1] = screen_edge['bottom']
						toffset[1] = ( srf.get_height() + 2 ) * -1
					
					pointlist = [ origin, [ origin[0] + 5, origin[1] ], [ origin[0], origin[1] + 5 ] ]
					
					pygame.draw.polygon( screen, [ 0, 0, 0 ], pointlist )
					
					global_.screen.blit( srf, [ origin[0] + toffset[0], origin[1] + toffset[1] ] )

global_.players = {}
global_.cid = 0