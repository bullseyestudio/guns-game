#!/usr/bin/env python

import sys
import socket, select

sys.path.append('./modules')
sys.path.append('../common/modules')

import constants
import edicomm
import gui
import network_comms
import input_handler
import battle

if len(sys.argv) < 3:
	sys.stderr.write('Usage: client.py username server\r\n')
	sys.exit(2)

constants.username = sys.argv[1]
constants.host = sys.argv[2]

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

gui.init_display()
network_comms.open()
input_handler.init_joy( 0 )

battle.init()

network_comms.send( edicomm.encode( 'UST', 'token_{0}'.format( constants.username ) ) )

while not gui.done:
	gui.event_loop()
