#!/usr/bin/env python

import sys, os, signal
os.environ["SDL_VIDEODRIVER"] = "dummy"

try:
	import pygame
	from pygame.locals import *
except ImportError:
	sys.stderr.write("Sorry, you absolutely MUST have pygame.\r\nTry sudo apt-get install python-pygame, if you're on a deb-system.\r\n")
	sys.exit(1)

from modules import server

server.init()

def _ctrlc_handler(*args):
	print 'Ctrl+C recognized. Stopping server...'

	server.quitting = True
	pygame.event.post(pygame.event.Event(QUIT))

signal.signal(signal.SIGINT, _ctrlc_handler)
print 'Ctrl+C catcher ready.'

c = pygame.time.Clock()
while not server.quitting:
	elapsed = c.tick(60)

	server.timer_tick(elapsed)

	if pygame.event.peek(pygame.QUIT):
		server.quitting = True

	pygame.event.clear()

server.exit()
