import network_comms, player, constants, battle
from modules import edicomm

import time

def init():
	pass

def tick():
	get_lobby_updates()

def get_lobby_updates():
	data = network_comms.lobby.read()

	if len( data ) == 0:
		return

	dlines = data.split( "\n" )
	for i in dlines:
		EDIDecoder( edicomm.decode( i ) )
	return

def EDIDecoder( EDIargs ):
	print EDIargs
	if   EDIargs[0] == 'ERR':
		#TODO: put in some error handling
#		print "We got an error code from the server"
		pass
	elif EDIargs[0] == 'MSG':
		pass
#		print 'Message to everyone.'
	elif EDIargs[0] == 'MST':
		pass
#		print 'Message to team'
	elif EDIargs[0] == 'UST':
		time.sleep(1);
		print 'Got UST ({0})! Bouncing to battle server.'.format(EDIargs[1])
		network_comms.battle.send( edicomm.encode('UST',EDIargs[1]) )
	elif EDIargs[0] == 'UID':
		# print EDIargs
		p = player.find_by_name( constants.username )
		if p != None:
			print 'WTF, we got 2 ID\'s'
			p.id = int( EDIargs[1] )
		else:
			plr = player.Player( constants.username )
			plr.position[0] = 0
			plr.position[1] = 0
			plr.id = int( EDIargs[ 1 ] )
			player.all[ int( EDIargs[ 1 ] ) ] = plr
			battle.cplr = plr
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
	elif EDIargs[0] == 'USD':
		p = player.find_by_id( int( EDIargs[1] ) )
		print '{p.name} disconnected!'.format(p=p)
		if not p == None:
			del player.all[ p.id ]

	else:
		pass
#		print 'Errrr...'
	return
