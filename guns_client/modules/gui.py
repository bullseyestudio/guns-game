import pygame
from pygame.locals import *

import sys

import battle
import network_comms
import constants
import input_handler
import edicomm
import bullet, waypoint
import player

width = 1024
height = 576
done = False

screen = None
background = None
font = None

zoom = 1.0
zoom_step = 0.0625


def init_display( ):
	""" Initialize display """

	global screen, font, background

	pygame.init()
	try:
		settings = open( "settings.cfg", "r+" )
		for line in settings:
			line = line.strip()
			key,value = line.split( "=" )
			if key == "WIDTH":
				width = int( value )
			if key == "HEIGHT":
				height = int( value )
		settings.close
	except IOError:
		width = 1024
		height = 576
		print "No configuration file found, using the defaults"

	font = pygame.font.Font(None, 18)

	screen = pygame.display.set_mode( ( width, height ), RESIZABLE )
	pygame.display.set_caption( "Client App" )
	pygame.time.set_timer( constants.PGE_GAMETICK, 20 )

	background = pygame.Surface( screen.get_size() )
	background = background.convert()
	background.fill( ( 250, 250, 250 ) )

	screen.blit( background, (0, 0) )
	pygame.display.flip()

def close_display():
	pygame.quit()

def draw_things():
	global background, screen

	battle.tick()

	screen.blit( background, (0, 0) )

	for p in player.all.itervalues():
		p.redraw( screen )

	for b in bullet.all:
		b.redraw( screen )

	for wp in waypoint.all:
		wp.redraw( screen )

	pygame.display.flip()


def event_loop():
	global screen, done

	for event in pygame.event.get():
		if event.type == constants.PGE_GAMETICK:
			draw_things()
		elif event.type in ( JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN ):
			input_handler.joystick( event )
		elif event.type in ( KEYDOWN, KEYUP ):
			input_handler.keyboard( event )
		elif event.type == MOUSEBUTTONDOWN:
			input_handler.mouse( event )
		elif event.type == VIDEORESIZE:
			screen = pygame.display.set_mode( event.size, RESIZABLE )
			battle.init();
			network_comms.send( edicomm.encode( 'USR', event.size ) )
		elif event.type == QUIT:
			network_comms.close()
			pygame.time.set_timer( constants.PGE_GAMETICK, 0 )
			done = True
			close_display()
			sys.exit(0)
