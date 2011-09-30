import pygame
from pygame.locals import *

from battle import players # /list needs this

def quit_handler(str, cl):
	pygame.event.post(pygame.event.Event(QUIT))

	cl.post_quit()

def help_handler(str, cl):
	parts = str.split(' ', 2)

	if len(parts) == 1:
		print 'list\t\tList players known to the server.'
		print 'forget\t\tMakes the server forget a player.'
		print 'help\t\tThis help text.'
		print 'quit\t\tStops the server.'
		print 'Try "help command" for more info on "command".'
	else:
		if parts[1].lower() == 'help':
			print 'Usage: help [command]\n'
			print 'Provides a list of commands, or help on a specific command.'
			print 'The [command] argument is optional.'
		elif parts[1].lower() == 'list':
			print 'Usage: list\n'
			print 'Returns an ugly list of all the players on the server.'
		elif parts[1].lower() == 'forget':
			print 'Usage: forget <name>\n'
			print 'Lets you tell the server to forget a player. Forgotten players need to re-authenticate if they want to talk to the server again.'
			print 'Will match partial names (e.g. "na" will match "narc"), and refuse to do anything if name is ambiguous.'
		elif parts[1].lower() == 'quit':
			print 'Usage: quit\n'
			print 'Stops the server immediately.'

def list_handler(str, cl):
	print 'ID\tusername\taddress info'
	for p in players.itervalues():
		print p.id, '\t', p.name, '\t', p.addr

def forget_handler(str, cl):
	parts = str.split(' ', 2)

	if len(parts) == 1:
		print 'Missing argument, try "help forget" for usage info.'
		return

	found_id = None

	for p in players.itervalues():
		if p.name.lower() == parts[1].lower(): #exact match!
			found_id = p.id
			break
		elif p.name.lower().startswith(parts[1].lower()):
			if found_id != None:
				print 'Ambiguous prefix, found', players[found_id].name, 'and', p.name, 'both matching', parts[1]
				found_id = None
				return
			else:
				found_id = p.id

	# TODO: Shouldn't be poking around other modules' internals like this
	# TODO: Should notify player of being kicked
	print 'Forgetting player', players[found_id].name
	del players[found_id]



handlers = { 'help': help_handler,
	'quit': quit_handler,
	'stop': quit_handler,
	'list': list_handler,
	'forget': forget_handler
}
