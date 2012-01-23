import pygame
from pygame.locals import *

from battle import player, waypoint, network
from battle.locals import PlayerAmbiguityError # can be raised by player name finder
from modules import edicomm
from modules.server import lobby, config

import urllib


def quit_handler(str, cl):
	pygame.event.post(pygame.event.Event(QUIT))

	cl.post_quit()

def help_handler(str, cl):
	parts = str.split(' ', 2)

	if len(parts) == 1:
		print 'say\t\tBroadcast a message to all players.'
		print 'list\t\tList players known to the server.'
		print 'forget\t\tMakes the server forget a player.'
		print 'help\t\tThis help text.'
		print 'wp\t\tList/add/move/remove waypoints.'
		print 'quit\t\tStops the server.'
		print 'register\tRegister the server at guns-game.com.'
		print 'Try "help command" for more info on "command".'
	else:
		if parts[1].lower() == 'say':
			print 'Usage: say <something>\n'
			print 'Sends <something> to all players on the server.'
		elif parts[1].lower() == 'list':
			print 'Usage: list\n'
			print 'Returns an ugly list of all the players on the server.'
		elif parts[1].lower() == 'forget':
			print 'Usage: forget <name>\n'
			print 'Lets you tell the server to forget a player. Forgotten players need to re-authenticate if they want to talk to the server again.'
			print 'Will match partial names (e.g. "na" will match "narc"), and refuse to do anything if name is ambiguous.'
		elif parts[1].lower() == 'help':
			print 'Usage: help [command]\n'
			print 'Provides a list of commands, or help on a specific command.'
			print 'The [command] argument is optional.'
		elif parts[1].lower() == 'wp':
			print 'Usage: wp [id [x,y title]]\n'
			print 'Without any parameters, gives you a list of all the waypoints known to the server.'
			print 'If passed a waypoint ID, will attempt to delete that waypoint, if it exists.'
			print 'If passed waypoint ID and a set of coordinates and a title, will attempt to create/move/rename a waypoint with that ID.'
		elif parts[1].lower() == 'quit':
			print 'Usage: quit\n'
			print 'Stops the server immediately.'
		elif parts[1].lower() == 'register':
			print 'Usage: register [secret]\n'
			print 'Without any parameters, tells you if your server is registered at guns-game.com.'
			print 'If passed a server secret (get one from meta.guns-game.com), it will update the server name and private key using data from the guns-game.com database.'

def list_handler(str, cl):
	print 'ID\tusername\taddress info\ttoken'
	for p in player.all:
		display_name = p.name
		if not p.ready:
			display_name = p.name + ' (inactive)'

		print p.id, '\t', display_name, '\t', p.addr, '\t', p.token

	print 'Known tokens: ', ", ".join(player.tokens)

def forget_handler(str, cl):
	parts = str.split(' ', 2)

	if len(parts) == 1:
		print 'Missing argument, try "help forget" for usage info.'
		return

	try:
		p = player.by_partial_name(parts[1])
	except PlayerAmbiguityError as e:
		print 'Found two players with same partial name: {e.p_one.name} and {e.p_two.name}'.format(e=e)
		return

	if not p:
		print 'Couldn\'t find player with prefix', parts[1]
		return

	# TODO: Should notify player of being kicked

	print 'Forgetting player', p.name
	network.to_ready( edicomm.encode( 'USD', p.id, 'Player kicked.' ) )
	player.all.remove(p)

def wp_handler(str, cl):
	parts = str.split(' ', 4)

	if len(parts) == 1: # Just wp by itself lists waypoints
		print 'ID\ttitle\tposition'
		for wp in waypoint.all:
			print wp.id, '\t', wp.title, '\t', wp.position
	elif len(parts) == 2: # wp <wpid> deletes waypoints
		wpid = int(parts[1])
		wp = waypoint.by_id(wpid)

		if not wp:
			print 'No waypoint with id {0}'.format(wpid)
			return

		print 'Deleting waypoint {wp.id} at {wp.position} titled {wp.title}'.format(wp=wp)

		waypoint.all.remove(wp)
		network.to_ready(edicomm.encode('WPT', wpid))
	elif len(parts) == 4: # wp <id> <x,y> <title> makes/moves waypoints
		wpid = int(parts[1])
		wppos = [int(x) for x in parts[2].split(',')]
		wptitle = parts[3]

		wp = waypoint.by_id(wpid)

		if not wp:
			wp = waypoint.Waypoint(wpid, wppos, wptitle)
			waypoint.all.append(wp)

		wp.position = wppos
		wp.title = wptitle

		print 'Created/moved/named waypoint {wp.id} at {wp.position} titled {wp.title}'.format(wp=wp)

		network.to_ready(edicomm.encode('WPT', wpid, wppos, wptitle))

def say_handler(str, cl):
	parts = str.split(' ', 1)

	if len(parts) == 1:
		print 'Missing argument, try "help say" for usage info.'
		return

	# HACK: Need a better way to handle this, this is NOT thread-safe
	lobby.server.d.global_chat('[CONSOLE]', parts[1])

def register_handler(str, cl):
	from modules.server import auth

	parts = str.split(' ', 1)

	if len(parts) == 1:
		if auth.key != None:
			print 'Server registered with name "{0}"'.format(config.cp.get('auth', 'server_name'))
		else:
			print 'Server is anonymous (not registered at guns-game.com)'

	else:
		secret = urllib.quote(parts[1])
		url = 'http://meta.guns-game.com/key/server/private/' + secret

		try:
			fh = urllib.urlopen(url)
			headers = fh.info()
			key = fh.read(4096)
			fh.close()

		except Exception, e:
			print 'Whoops, that didn\'t work! Problem:', e
			return

		if(fh.getcode() != 200):
			print 'Error fetching private key. Server said:', key
			return

		sname = headers['X-Your-Server-Name']
		config.cp.set('auth', 'server_name', sname)

		try:
			fh = open(config.cp.get('auth', 'private_key_path'), 'wb')
			fh.write(key)
			fh.close()
		except Exception, e:
			print 'Error writing private key file:', e
			return

		auth.init()

		print 'Server name is now "{0}" and private key is set.'.format(sname)


handlers = { 'help': help_handler,
	'quit': quit_handler,
	'list': list_handler,
	'forget': forget_handler,
	'wp': wp_handler,
	'say': say_handler,
	'register': register_handler,
}
