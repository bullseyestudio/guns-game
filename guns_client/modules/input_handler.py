import pygame
from pygame.locals import *

import network_comms
import constants
import edicomm
import waypoint

def init_joy( joynum ):
	constants.joystick_count = pygame.joystick.get_count()

	if constants.joystick_count == 0:
		print "No joysticks detected, joystick support not enabled."
	else:
		constants.my_joystick = pygame.joystick.Joystick( joynum )
		constants.my_joystick.init()
		print constants.my_joystick.get_numaxes() , " Axis Joystick found"
		if constants.my_joystick.get_numaxes() < 2:
			constants.joystick_count = 0
			print "Joystick with less than 2 axis not supported at the moment"

def mouse( event ):
	if(event.button == 1): # left click
		pos = ( constants.cplr.position[0] + int( ( event.pos[0] - ( constants.screen.get_width() /2 ) ) / constants.zoom ), constants.cplr.position[1] + int( ( event.pos[1] - ( constants.screen.get_height() /2 ) ) / constants.zoom ) )
		network_comms.send( edicomm.encode( 'USF', pos ) )
	elif event.button == 3: # right click
		pos = ( constants.cplr.position[0] + int( ( event.pos[0] - ( constants.screen.get_width() /2 ) ) / constants.zoom ), constants.cplr.position[1] + int( ( event.pos[1] - ( constants.screen.get_height() /2 ) ) / constants.zoom ) )

		deleting = False
		for wp in waypoint.all:
			if wp.is_within(pos):
				deleting = True
				break

		if deleting:
			network_comms.send( edicomm.encode( 'WPT' ) )
		else:
			network_comms.send( edicomm.encode( 'WPT', pos ) )
	elif(event.button == 4): # mouse wheel down
		constants.zoom += constants.zoom_step
		if(constants.zoom > 1):
			constants.zoom = 1
		else:
			network_comms.send( edicomm.encode( 'USZ', constants.zoom ) )
	elif(event.button == 5): # mouse wheel up
		constants.zoom -= constants.zoom_step
		if(constants.zoom < constants.min_zoom):
			constants.zoom = constants.min_zoom
		else:
			network_comms.send( edicomm.encode( 'USZ', constants.zoom ) )
	else:
		print 'Unhandled mouse button at ({0},{1}) btn:{2}'.format( pos[0], pos[1], event.button )

def keyboard( event ):
	move = False
	veldelta = 50

	#print '{0}:{1}'.format( event.type, event.key )

	if event.type == KEYDOWN:
		step = 0.0625
		# TODO: Add in keyboard shortcuts to zoom
		if event.key == K_s:
			constants.velocity[1] += veldelta
			move = True
		elif event.key == K_w:
			constants.velocity[1] -= veldelta
			move = True
		elif event.key == K_d:
			constants.velocity[0] += veldelta
			move = True
		elif event.key == K_a:
			constants.velocity[0] -= veldelta
			move = True
		elif event.key == K_z:
			constants.velocity = [0, 0]
			move = True
		elif event.key == K_KP_PLUS:
			constants.zoom += step
			if(constants.zoom > 1):
				constants.zoom = 1
			else:
				network_comms.send( edicomm.encode( 'USZ', constants.zoom ) )
				return
		elif event.key == K_KP_MINUS:
			constants.zoom -= step
			if(constants.zoom < step):
				constants.zoom = step
			else:
				network_comms.send( edicomm.encode( 'USZ', constants.zoom ) )
				return
	elif event.type == KEYUP:
		if event.key == K_s:
			constants.velocity[1] -= veldelta
			move = True
		elif event.key == K_w:
			constants.velocity[1] += veldelta
			move = True
		elif event.key == K_d:
			constants.velocity[0] -= veldelta
			move = True
		elif event.key == K_a:
			constants.velocity[0] += veldelta
			move = True

	if(move == True):
		network_comms.send( edicomm.encode( 'USV', constants.velocity ) )

def joystick( event ):
	#print "Joy event :)"
	if constants.joystick_count != 0:
		constants.velocity[0] = int( constants.my_joystick.get_axis( 0 ) * 50 )
		constants.velocity[1] = int( constants.my_joystick.get_axis( 1 ) * 50 )

		newrot = degrees( atan2( constants.my_joystick.get_axis( 2 ), constants.my_joystick.get_axis( 3 ) ) )

		network_comms.send( edicomm.encode( 'USV', constants.velocity ) )
