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
import pygame
from pygame.locals import *

pygame.display.init()
screen = pygame.display.set_mode((1,1))

import cmdline

cl = cmdline.cmdline()

print 'Server init begins.'

def quit_handler(str):
	pygame.event.post(pygame.event.Event(QUIT))

cl.add_command('quit', quit_handler)

def help_handler(str):
	parts = str.split(' ', 2)

	if len(parts) == 1:
		print 'help\t\tThis help text.'
		print 'quit\t\tStops the server.'
		print 'Try "help command" for more info on "command".'
	else:
		if parts[1].lower() == 'help':
			print 'Usage: help [command]\n'
			print 'Provides a list of commands, or help on a specific command.'
			print 'The [command] argument is optional.'
		elif parts[1].lower() == 'quit':
			print 'Usage: quit\n'
			print 'Stops the server immediately.'

cl.add_command('help', help_handler)

print 'Waiting for commands, type "quit" to stop the server.'
cl.start_listener()

pygame.time.set_timer(USEREVENT+1, 1000)

while True:
	for event in pygame.event.get():
		if event.type == USEREVENT+1:
			battle.timer_tick()
			cl.handle_command()
		elif (event.type == QUIT):
			sys.exit(0)

