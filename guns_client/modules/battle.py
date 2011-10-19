import pygame
from pygame.locals import *

import player
import waypoint
import edicomm
import network_comms
import constants
import test_rot
import bullet
import gui # A sign of: we do screen fuckery here!

cplr = None

def init():
	pass

def tick():
	get_player_updates()

def get_player_updates():
	data = network_comms.read()

	if len( data ) == 0:
		return

	dlines = data.split( "\n" )
	for i in dlines:
		EDIDecoder( edicomm.decode( i ) )
	return

def EDIDecoder( EDIargs ):

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
		p = player.find_by_name( constants.username )
		if not p == None:
			print 'WTF, we got 2 ID\'s'
			p.id = int( EDIargs[1] )
		else:
			plr = player.Player( constants.username )
			plr.position[0] = 0
			plr.position[1] = 0
			plr.id = int( EDIargs[ 1 ] )
			player.all[ int( EDIargs[ 1 ] ) ] = plr

		network_comms.send( edicomm.encode( 'USN', constants.username ) )
	elif EDIargs[0] == 'USN':
		p = player.find_by_name( EDIargs[ 2 ] )
		if not p == None:
			del player.all[ p.id ]
		p = player.Player( EDIargs[ 2 ] )
		p.position[0] = 0
		p.position[1] = 0
		p.rotation = 0
		p.id = int( EDIargs[ 1 ] )
		player.all[ int( EDIargs[1] ) ] = p
	elif EDIargs[0] == 'USP':
		try:
			p = player.all[ int( EDIargs[1] ) ]
			if not p == None:
				p.position[0] = int( EDIargs[2][0] )
				p.position[1] = int( EDIargs[2][1] )
				p.rotation = float( EDIargs[3] )
				p.draw = True
		except:
			pass
	elif EDIargs[0] == 'USD':
		p = player.find_by_id( int( EDIargs[1] ) )
		if not p == None:
			del player.all[ p.id ]
	elif EDIargs[0] == 'NPV':
		p = player.find_by_id( int( EDIargs[1] ) )
		if not p == None:
			p.draw = False
	elif EDIargs[0] == 'WPT':
		if len(EDIargs) >= 4: # Setting a waypoint (WPT id x,y title [owner-id])
			wpid = int(EDIargs[1])
			wppos = [int(x) for x in EDIargs[2]]
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
