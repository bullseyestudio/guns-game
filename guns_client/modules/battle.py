import pygame
from pygame.locals import *

import player
import waypoint
import edicomm
import network_comms
import constants
import test_rot
import bullet

players = {}

def init():
	constants.background = pygame.Surface( constants.screen.get_size() )
	constants.background = constants.background.convert()
	constants.background.fill( ( 250, 250, 250 ) )

	constants.screen.blit( constants.background, (0, 0) )
	pygame.display.flip()

def tick():
	get_player_updates()

	constants.screen.blit( constants.background, (0, 0) )

	for p in players.itervalues():
		p.redraw( constants.screen )

	for b in bullet.all:
		b.redraw( constants.screen )

	for wp in waypoint.all:
		wp.redraw( constants.screen )

#	test_rot.draw_rot()

	pygame.display.flip()

def get_player_updates():
	data = network_comms.read()

	if len( data ) == 0:
		return

	dlines = data.split( "\n" )
	for i in dlines:
		EDIDecoder( edicomm.decode( i ) )
	return

def EDIDecoder( EDI ):

	EDIargs = EDI

#	print EDIargs
	if   EDIargs[0] == 'ERR':
		#TODO: put in some error handling
#		print "We got an error code from the server"
		pass
	elif EDIargs[0] == 'LAG':
		pass
#		print 'Ping test, please.'
	elif EDIargs[0] == 'MSG':
		pass
#		print 'Message to everyone.'
	elif EDIargs[0] == 'MST':
		pass
#		print 'Message to team'
	elif EDIargs[0] == 'USC':
		pass
#		print 'Hey I should be a different colour'
	elif EDIargs[0] == 'USF':
		print EDIargs
		pos = EDIargs[2]
		b = bullet.Bullet( ( int( pos[0] ), int( pos[1] ) ) )
		bullet.all.append( b )
		pass
		# We be receving a fire pos update
	elif EDIargs[0] == 'UID':
		# print EDIargs
		p = constants.findPlayerByName( constants.username )
		if not p == None:
			print 'WTF, we got 2 ID\'s'
			p.id = int( EDIargs[1] )
		else:
			plr = player.Player( constants.username )
			plr.position[0] = 0
			plr.position[1] = 0
			plr.id = int( EDIargs[ 1 ] )
			players[ int( EDIargs[ 1 ] ) ] = plr

		network_comms.send( edicomm.encode( 'USN', constants.username ) )
	elif EDIargs[0] == 'USN':
		p = constants.findPlayerByName( EDIargs[ 2 ] )
		if not p == None:
			del players[ p.id ]
		p = player.Player( EDIargs[ 2 ] )
		p.position[0] = 0
		p.position[1] = 0
		p.rotation = 0
		p.id = int( EDIargs[ 1 ] )
		players[ int( EDIargs[1] ) ] = p
	elif EDIargs[0] == 'USP':
		try:
			p = players[ int( EDIargs[1] ) ]
			if not p == None:
				p.position[0] = int( EDIargs[2][0] )
				p.position[1] = int( EDIargs[2][1] )
				p.rotation = float( EDIargs[3] )
				p.draw = True
		except:
			pass
	elif EDIargs[0] == 'USD':
		p = constants.findPlayerById( int( EDIargs[1] ) )
		if not p == None:
			del players[ p.id ]
	elif EDIargs[0] == 'NPV':
		p = constants.findPlayerById( int( EDIargs[1] ) )
		if not p == None:
			p.draw = False
	elif EDIargs[0] == 'WPT':
		if len(EDIargs) == 4: # Setting a waypoint (WPT id x,y title)
			wpid = int(EDIargs[1])
			wppos = [int(x) + y for x,y in zip(EDIargs[2], (-8,8))]
			wptitle = EDIargs[3]

			wp = waypoint.find_waypoint_by_id(wpid)

			if wp:
				wp.name = wptitle
				wp.position = wppos
			else:
				waypoint.all.append(waypoint.Waypoint(wpid, wppos, wptitle))
		elif len(EDIargs) == 2: # Removing a waypoint (WPT id)
			wpid = int(EDIargs[1])
			wp = waypoint.find_waypoint_by_id(wpid)

			if wp:
				waypoint.all.remove(wp)
		else:
			print 'Weird shit happened and we got a malformed WPT: {0}'.format(edicomm.encode(EDIargs))

	else:
		pass
#		print 'Errrr...'
	return
