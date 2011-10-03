
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

def keyboard( event ):
	move = False
	
	print '{0}:{1}'.format( event.type, event.key )
	
	if event.type == KEYDOWN:
		if event.key == K_s:
			global_.velocity[1] = 50
		elif event.key == K_w:
			global_.velocity[1] = -50
		elif event.key == K_a:
			global_.velocity[0] = -50
		elif event.key == K_d:
			global_.velocity[0] = 50
		elif event.key == K_z:
			global_.velocity = [0, 0]
		elif event.key == K_x:
			print global_.players.items()
	elif event.type == KEYUP:
		if event.key in [K_s, K_w, K_a, K_d]:
			global_.velocity = [0, 0]
			
	network_comms.send( edicomm.encode( 'USV', global_.velocity ) )

def joystick( event ):
	#print "Joy event :)"
	global_.velocity[0] = int( global_.my_joystick.get_axis( 0 ) * 50 )
	global_.velocity[1] = int( global_.my_joystick.get_axis( 1 ) * 50 )
	network_comms.send( edicomm.encode( 'USV', global_.velocity ) )

