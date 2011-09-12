#!/usr/bin/env python

import sys

sys.path.append('./modules')
sys.path.append('../common/modules')

import edicomm
import physim

import lobby
import battle
import auth

import cmdline

cl = cmdline.cmdline()

class QuitException(Exception):
	pass

print 'Server init begins.'

def quit_handler(str):
	raise QuitException()

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

cl.start_listener()
print 'Waiting for commands, type "quit" to stop the server.'
while True:
	try:
		cl.handle_command()
	except QuitException:
		print 'Server shutting down.'
		break
