import pygame
from pygame.locals import *

import constants
import battle
import gui

size = (16, 16)
offset = (-8, -8) # Necessary offset to draw the waypoint centered at position,
                # instead of with the position in a corner.

class Waypoint:
	def __init__(self, id, pos, name):
		global size
		self.id = id
		self.name = name
		self.position = pos
		self.textcolor = ( 10, 10, 10 )
		self.srf = pygame.Surface( size )
		self.srf.fill( ( 0, 0, 0 ) )
		self.text = gui.font.render( self.name, 1, self.textcolor )
		self.text_rect = self.text.get_rect()
		self.screen_pos = [-16,-16] # Magic offscreen coordinates

	def redraw(self, screen):
		global offset

		spos = gui.map_to_screen(self.position)

		if( gui.is_onscreen(self.position) ):
			toff = (0, -16)
			tpos = [ a + b - c for a,b,c in zip(spos, toff, self.text_rect.center)]

			spos = [a + b for a,b in zip(spos, offset)]

			self.screen_pos = spos

			gui.screen.blit( self.srf, spos )
			gui.screen.blit( self.text, tpos )
		else:
			self.screen_pos = [-16, -16]

			posx = spos[0]
			posy = spos[1]
			toffx = 0
			toffy = 0

			if posx < 0:
				posx = 0
				toffx = 10 + self.text_rect.centerx
			elif posx > (gui.screen_rect.width):
				posx = gui.screen_rect.width
				toffx = -10 - self.text_rect.centerx

			if posy < 0:
				posy = 0
				toffy = 10 + self.text_rect.centery
			elif posy > (gui.screen_rect.height):
				posy = gui.screen_rect.height
				toffy = -10 - self.text_rect.centery

			spos = (posx, posy)
			toff = (toffx, toffy)
			tpos = [ a + b - c for a,b,c in zip(spos, toff, self.text_rect.center)]

			spos = [ a + b for a,b in zip(spos, offset)]

			gui.screen.blit( self.srf, spos )
			gui.screen.blit( self.text, tpos )

	def contains(self, pos):
		global size
		boundBox = pygame.Rect( ( self.position[0] - ( size[0] / 2 ), self.position[1] - ( size[1] / 2 ) ), size)
		return boundBox.collidepoint( pos )

def find_waypoint_by_id(id):
	for wp in all:
		if wp.id == id:
			return wp

all = []
