
import sys

sys.path.append('./modules')
sys.path.append('../common/modules')

import network_comms
import global_
import edicomm

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

def init_joy( joynum ):
	global_.joystick_count = pygame.joystick.get_count()

	if global_.joystick_count == 0:
		print "No joysticks detected, joystick support not enabled."
	else:
		global_.my_joystick = pygame.joystick.Joystick( joynum )
		global_.my_joystick.init()
		print global_.my_joystick.get_numaxes() , " Axis Joystick found"
		if global_.my_joystick.get_numaxes() < 2:
			global_.joystick_count = 0
			print "Joystick with less than 2 axis not supported at the moment"

def mouse( event ):
	
	if(event.button >= 4):
		# we are scrolling the mouse wheel. Zoom event!
		step = 0.0625
		print 'step: {0}'.format( step )
		if(event.button == 5):
			global_.zoom -= step
			if(global_.zoom < step):
				global_.zoom = step
			else:
				network_comms.send( edicomm.encode( 'USZ', global_.zoom ) )
			print 'Scrolling positive: {0}'.format( global_.zoom )
		if(event.button == 4):
			global_.zoom += step
			if(global_.zoom > 1):
				global_.zoom = 1
			else:
				network_comms.send( edicomm.encode( 'USZ', global_.zoom ) )
			print 'Scrolling negative: {0}'.format( global_.zoom )
	else:
		pos = [ global_.cplr.position[0] + int( ( event.pos[0] - ( global_.screen.get_width() /2 ) ) / global_.zoom ), global_.cplr.position[1] + int( ( event.pos[1] - ( global_.screen.get_height() /2 ) ) / global_.zoom ) ]
		print '{0}:{1} -- btn:{2}'.format( pos[0], pos[1], event.button )
		network_comms.send( edicomm.encode( 'USF', pos ) )

def keyboard( event ):
	move = False

	print '{0}:{1}'.format( event.type, event.key )

	if event.type == KEYDOWN:
		step = 0.0625
		# TODO: Add in keyboard shortcuts to zoom
		if event.key == K_s:
			global_.velocity[1] += 50
			move = True
		elif event.key == K_w:
			global_.velocity[1] += -50
			move = True
		elif event.key == K_d:
			global_.velocity[0] += 50
			move = True
		elif event.key == K_a:
			global_.velocity[0] += -50
			move = True
		elif event.key == K_z:
			global_.velocity = [0, 0]
			move = True
		elif event.key == K_KP_PLUS:
			global_.zoom += step
			if(global_.zoom > 1):
				global_.zoom = 1
			else:
				network_comms.send( edicomm.encode( 'USZ', global_.zoom ) )
				return
		elif event.key == K_KP_MINUS:
			global_.zoom -= step
			if(global_.zoom < step):
				global_.zoom = step
			else:
				network_comms.send( edicomm.encode( 'USZ', global_.zoom ) )
				return
	elif event.type == KEYUP:
		if event.key == K_s:
			global_.velocity[1] += -50
			move = True
		elif event.key == K_w:
			global_.velocity[1] += 50
			move = True
		elif event.key == K_d:
			global_.velocity[0] += -50
			move = True
		elif event.key == K_a:
			global_.velocity[0] += 50
			move = True
			
	if(move == True):
		network_comms.send( edicomm.encode( 'USV', global_.velocity ) )

def joystick( event ):
	#print "Joy event :)"
	if global_.joystick_count != 0:
		global_.velocity[0] = int( global_.my_joystick.get_axis( 0 ) * 50 )
		global_.velocity[1] = int( global_.my_joystick.get_axis( 1 ) * 50 )
		
		newrot = degrees( atan2( global_.my_joystick.get_axis( 2 ), global_.my_joystick.get_axis( 3 ) ) )
		
		network_comms.send( edicomm.encode( 'USV', global_.velocity ) )
