#!/usr/bin/env python

import sys
import socket, select

sys.path.append('./modules')
sys.path.append('../common/modules')

import global_
from global_ import *
import edicomm
import os_gui
import network_comms
import input_handler
import battle

if len(sys.argv) < 3:
	sys.stderr.write('Usage: client.py username server\r\n')
	sys.exit(2)

global_.username = sys.argv[1]
global_.host = sys.argv[2]
global_.plr = None

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

os_gui.init_display()
network_comms.open()
input_handler.init_joy( 0 )

battle.init()

network_comms.send( 'USA {0}'.format( global_.username ) )

while not os_gui.done:
	os_gui.event_loop()
