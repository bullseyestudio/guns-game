import pygame
from pygame.locals import *

from modules import edicomm

from modules.client import network_comms, constants, waypoint, gui, battle

velocity = [0, 0]

joystick_count = 0
my_joystick = 0

def init_joy( joynum ):
	global joystick_count, my_joystick

	joystick_count = pygame.joystick.get_count()

	if joystick_count == 0:
		print "No joysticks detected, joystick support not enabled."
	else:
		my_joystick = pygame.joystick.Joystick( joynum )
		my_joystick.init()
		print my_joystick.get_numaxes() , " Axis Joystick found"
		if my_joystick.get_numaxes() < 2:
			joystick_count = 0
			print "Joystick with less than 2 axis not supported at the moment"

def mouse( event ):
	if(event.button == 1): # left click
		network_comms.battle.send( edicomm.encode( 'USF', gui.screen_to_map(event.pos) ) )
	elif event.button == 3: # right click
		pos = gui.screen_to_map(event.pos)

		if not battle.cplr.waypoint == None:
			if battle.cplr.waypoint.contains(pos):
				network_comms.battle.send( edicomm.encode( 'WPT' ) )
			else:
				print 'wp does not contain {0}'.format( pos )
				network_comms.battle.send( edicomm.encode( 'WPT', pos ) )
		else:
			print 'cplr.wp == None'
			network_comms.battle.send( edicomm.encode( 'WPT', pos ) )
	elif(event.button == 4): # mouse wheel down
		gui.zoom += gui.zoom_step
		if(gui.zoom > 1):
			gui.zoom = 1
		else:
			network_comms.battle.send( edicomm.encode( 'USZ', gui.zoom ) )
	elif(event.button == 5): # mouse wheel up
		gui.zoom -= gui.zoom_step
		if(gui.zoom < constants.min_zoom):
			gui.zoom = constants.min_zoom
		else:
			network_comms.battle.send( edicomm.encode( 'USZ', gui.zoom ) )
	else:
		print 'Unhandled mouse button at ({event.pos[0]},{event.pos[1]}) btn:{event.button}'.format( event=event )

def keyboard( event ):
	global velocity

	move = False
	veldelta = 50

	#print '{0}:{1}'.format( event.type, event.key )

	if event.type == KEYDOWN:
		step = 0.0625
		# TODO: Add in keyboard shortcuts to zoom
		if event.key == K_s:
			velocity[1] += veldelta
			move = True
		elif event.key == K_w:
			velocity[1] -= veldelta
			move = True
		elif event.key == K_d:
			velocity[0] += veldelta
			move = True
		elif event.key == K_a:
			velocity[0] -= veldelta
			move = True
		elif event.key == K_z:
			velocity = [0, 0]
			move = True
		elif event.key == K_KP_PLUS:
			gui.zoom += step
			if(gui.zoom > 1):
				gui.zoom = 1
			else:
				network_comms.battle.send( edicomm.encode( 'USZ', gui.zoom ) )
				return
		elif event.key == K_KP_MINUS:
			gui.zoom -= step
			if(gui.zoom < step):
				gui.zoom = step
			else:
				network_comms.battle.send( edicomm.encode( 'USZ', gui.zoom ) )
				return
	elif event.type == KEYUP:
		if event.key == K_s:
			velocity[1] -= veldelta
			move = True
		elif event.key == K_w:
			velocity[1] += veldelta
			move = True
		elif event.key == K_d:
			velocity[0] -= veldelta
			move = True
		elif event.key == K_a:
			velocity[0] += veldelta
			move = True

	if(move == True):
		network_comms.battle.send( edicomm.encode( 'USV', velocity ) )

def joystick( event ):
	#print "Joy event :)"
	if joystick_count != 0:
		velocity[0] = int( my_joystick.get_axis( 0 ) * 50 )
		velocity[1] = int( my_joystick.get_axis( 1 ) * 50 )

		newrot = degrees( atan2( my_joystick.get_axis( 2 ), my_joystick.get_axis( 3 ) ) )

		network_comms.battle.send( edicomm.encode( 'USV', velocity ) )
