import pygame
from pygame.locals import *

from battle import players, tokens, waypoints, Waypoint, wp_idx_by_id, wp_by_id, sock # /list needs this
import edicomm

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
		print 'listwp\t\tList waypoints.'
		print 'addwp\t\tAdds a waypoint to the list.'
		print 'delwp\t\tRemoves a waypoint from the list.'
		print 'Try "help command" for more info on "command".'
	else:
		if parts[1].lower() == 'help':
			print 'Usage: help [command]\n'
			print 'Provides a list of commands, or help on a specific command.'
			print 'The [command] argument is optional.'
		elif parts[1].lower() == 'list':
			print 'Usage: list\n'
			print 'Returns an ugly list of all the players on the server.'
		elif parts[1].lower() == 'listwp':
			print 'Usage: listwp\n'
			print 'Returns an ugly list of all the waypoints on the server.'
		elif parts[1].lower() == 'forget':
			print 'Usage: forget <name>\n'
			print 'Lets you tell the server to forget a player. Forgotten players need to re-authenticate if they want to talk to the server again.'
			print 'Will match partial names (e.g. "na" will match "narc"), and refuse to do anything if name is ambiguous.'
		elif parts[1].lower() == 'quit':
			print 'Usage: quit\n'
			print 'Stops the server immediately.'
		elif parts[1].lower() == 'listwp':
			print 'Usage: listwp\n'
			print 'Lists all waypoints in an ugly list.'
		elif parts[1].lower() == 'addwp':
			print 'Usage: addwp <title> <posx> <posy>\n'
			print 'Adds a named waypoint to the list at position specified.'
		elif parts[1].lower() == 'delwp':
			print 'Usage: delwp <id>\n'
			print 'Deletes waypoint with specified id (Player-owned waypoints are id 257 and above).'

def list_handler(str, cl):
	print 'ID\tusername\taddress info\ttoken'
	for p in players:
		print p.id, '\t', p.name, '\t', p.addr, '\t', p.token

	print 'Known tokens: ', ", ".join(tokens)

def forget_handler(str, cl):
	parts = str.split(' ', 2)

	if len(parts) == 1:
		print 'Missing argument, try "help forget" for usage info.'
		return

	found_id = None

	for p in players:
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
	if found_id == None:
		print 'Couldn\'t find player with prefix', parts[1]
		return

	print 'Forgetting player', players[found_id].name
	del players[found_id]

def listwp_handler(str, cl):
	print 'ID\ttitle\tposition'
	for w in waypoints:
		print w.id, '\t', w.title, '\t', w.position

def addwp_handler(str, cl):
	#   0      1       2      3
	# addwp <title> <posx> <posy>
	parts = str.split( ' ', 4)
	
	wppos = ( parts[2], parts[3] )
	wptitle = parts[1]
	
	wpid = None
	for x in range(1,257):
		w = wp_by_id( x )
		if w == None:
			wpid = x
			break
	
	if not wpid == None:	
		w = Waypoint( wpid, wppos, wptitle )
		waypoints.append( w )
		
		data = edicomm.encode('WPT', wpid, wppos, wptitle )
		print data
		for p in players:
			if p.name != '':
				sock.sendto(data, p.addr)
		

def delwp_handler(str, cl):
	# delwp <wpid>
	parts = str.split( ' ', 2 )
	
	wpidx = wp_idx_by_id( int( parts[1] ) )
	wpid = waypoints[ wpidx ].id
	
	del waypoints[ wpidx ]
	
	data = edicomm.encode('WPT', wpid )
	print data
	for p in players:
		if p.name != '':
			sock.sendto(data, p.addr)

handlers = { 'help': help_handler,
	'quit': quit_handler,
	'stop': quit_handler,
	'list': list_handler,
	'forget': forget_handler,
	'listwp': listwp_handler,
	'addwp': addwp_handler,
	'delwp': delwp_handler
}
