
import sys

sys.path.append('./modules')
sys.path.append('../common/modules')

import battle
import network_comms
import global_
import input_handler
import edicomm

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)
	
width = 1024
height = 576
done = False

def init_display( ):
	# Initialise screen
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
	
	global_.font = pygame.font.Font(None, 18)
	global_.screen = pygame.display.set_mode( ( width, height ), RESIZABLE )
	pygame.display.set_caption( "Client App" )
	pygame.time.set_timer( global_.PGE_GAMETICK, 20 )
	
def close_display():
	pygame.quit()

def event_loop():
	for event in pygame.event.get():
		if event.type == global_.PGE_GAMETICK:
			battle.tick()
		elif event.type in ( JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN ):
			input_handler.joystick( event )
		elif event.type in ( KEYDOWN, KEYUP ):
			input_handler.keyboard( event )
		elif event.type == MOUSEBUTTONDOWN:
			input_handler.mouse( event )
		elif event.type == VIDEORESIZE:
			global_.screen = pygame.display.set_mode( event.size, RESIZABLE )
			battle.init();
			network_comms.send( edicomm.encode( 'USR', event.size ) )
		elif event.type == QUIT:
			network_comms.close()
			pygame.time.set_timer( global_.PGE_GAMETICK, 0 )
			global_.done = True
			close_display()
			sys.exit(0)
