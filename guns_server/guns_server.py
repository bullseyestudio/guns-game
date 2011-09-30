#!/usr/bin/env python

import sys, os

sys.path.append('./modules')
sys.path.append('../common/modules')

import edicomm
import physim

import lobby
import battle
import auth

os.environ["SDL_VIDEODRIVER"] = "dummy"

try:
	import pygame
	from pygame.locals import *
except ImportError:
	sys.stderr.write("Sorry, you absolutely MUST have pygame.\nTry sudo apt-get install python-pygame, if you're on a deb-system.\n")
	sys.exit(1)

pygame.display.init()
screen = pygame.display.set_mode((1,1))

print 'Server init begins.'

## Command-line init stuff
import cmdline
cl = cmdline.cmdline()

import cmdhandlers
for k, h in cmdhandlers.handlers.iteritems():
	cl.add_command(k, h)

print 'Waiting for commands, type "quit" to stop the server.'
cl.start_listener()

pygame.time.set_timer(USEREVENT+1, 100)

while True:
	for event in pygame.event.get():
		if event.type == USEREVENT+1:
			battle.timer_tick()
			cl.handle_command()
		elif (event.type == QUIT):
			sys.exit(0)
