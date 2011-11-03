#!/usr/bin/env python

import sys, os, signal

from modules import edicomm
from modules.server import battle, cmdline, cmdhandlers, lobby
from modules.server.battle import queue

os.environ["SDL_VIDEODRIVER"] = "dummy"

try:
	import pygame
	from pygame.locals import *
except ImportError:
	sys.stderr.write("Sorry, you absolutely MUST have pygame.\r\nTry sudo apt-get install python-pygame, if you're on a deb-system.\r\n")
	sys.exit(1)

pygame.display.init()
screen = pygame.display.set_mode((1,1))

print 'Server init begins.'

lobby.start_server()

cl = cmdline.cmdline()
for k, h in cmdhandlers.handlers.iteritems():
	cl.add_command(k, h)
cl.start_listener()

def ctrlc_handler(*args):
	print 'Ctrl+C recognized.'

	pygame.event.post(pygame.event.Event(QUIT))

signal.signal(signal.SIGINT, ctrlc_handler)

# This guy makes sure everything ticks
pygame.time.set_timer(USEREVENT+1, 25)

while True:
	for event in pygame.event.get():
		if event.type == USEREVENT+1:
			battle.timer_tick()
			queue.tick()
			cl.handle_command()
		elif (event.type == QUIT):
			cl.post_quit()
			sys.exit(0)
