#!/usr/bin/env python

import sys, time

try:
	import pygame
	import pygame._view # Py2exe needs this, else it won't include _view
	from pygame.locals import *
except ImportError:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

pygame.init()

from modules import client

client.init()

c = pygame.time.Clock()
while not client.quitting:
	elapsed = c.tick(60)

	client.tick(elapsed)

client.exit()
