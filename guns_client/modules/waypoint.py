import pygame
from pygame.locals import *

import constants
import battle
import gui

class Waypoint:
	def __init__(self, id, pos, name):
		self.id = id
		self.name = name
		self.position = ( int( pos[0]), int( pos[1] ) )
		self.textcolor = ( 10, 10, 10 )
		self.size = [ 16, 16 ]
		self.srf = pygame.Surface( ( self.size[0], self.size[1] ) )
		self.view_offset = { 'top':0, 'left':0, 'bottom':0, 'right':0}

	def redraw(self, screen):
		max_view_radius = ( ( int( screen.get_width() ) / float(gui.zoom) ) / 2,  ( int( screen.get_height() ) / float(gui.zoom) ) / 2 )
		selfpos = ( int( self.position[0] * gui.zoom) , int( self.position[1] * gui.zoom ) )
		plrpos = ( int( battle.cplr.position[0] * gui.zoom) , int( battle.cplr.position[1] * gui.zoom ) )
		srf2 = gui.font.render( self.name, 1, self.textcolor )

		# TODO: pleasefixkthxbai
		if(self.position[0] < ( battle.cplr.position[0] + max_view_radius[0] + self.view_offset['right'] )
		   and self.position[0] > ( battle.cplr.position[0] - max_view_radius[0] - self.view_offset['left'] )
		   and self.position[1] < ( battle.cplr.position[1] + max_view_radius[1] + self.view_offset['top'] )
		   and self.position[1] > ( battle.cplr.position[1] - max_view_radius[1] - self.view_offset['bottom'] )
		):
			offsetx = selfpos[0] - plrpos[0]
			offsety = selfpos[1] - plrpos[1]
			gui.screen.blit( self.srf, ( gui.screen.get_width() / 2 + offsetx, gui.screen.get_height() /2 - 15 + offsety ) )
			gui.screen.blit( srf2, ( gui.screen.get_width() / 2 + offsetx, gui.screen.get_height() /2 + offsety - 30 ) )
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
			origin = [ gui.screen.get_width() / 2 + offsetx, gui.screen.get_height() /2 - 15 + offsety ]

			toffset = [ 0, 0 ]

			if origin[0] < screen_edge['left']:
				origin[0] = screen_edge['left']
				toffset[0] = 20
			if origin[0] > screen_edge['right']:
				origin[0] = screen_edge['right']
				toffset[0] = ( srf2.get_width() + 10 ) * -1

			if origin[1] < screen_edge['top']:
				origin[1] = screen_edge['top']
				toffset[1] = 20
			if origin[1] > screen_edge['bottom']:
				origin[1] = screen_edge['bottom']
				toffset[1] = ( srf2.get_height() + 2 ) * -1

			pointlist = [ origin, [ origin[0] + self.size[0], origin[1] ], [ origin[0] + self.size[0], origin[1] + self.size[1] ], [ origin[0], origin[1] + self.size[1] ] ]

			pygame.draw.polygon( screen, [ 0, 0, 0 ], pointlist )

			gui.screen.blit( srf2, [ origin[0] + toffset[0], origin[1] + toffset[1] ] )

	def is_within(self, pos):
		if pos[0] > self.position[0] and pos[0] < ( self.position[0] + self.srf.get_width() ) and pos[1] < self.position[1] and pos[1] > ( self.position[1] - self.srf.get_height() ):
			return True
		else:
			return False

def find_waypoint_by_id(id):
	for wp in all:
		if wp.id == id:
			return wp

all = []
