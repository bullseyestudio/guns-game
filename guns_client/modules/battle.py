import sys

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

sys.path.append('./modules')
sys.path.append('../common/modules')

import player
from player import *
import edicomm
import network_comms
import global_
from global_ import *

def init():
	global_.background = pygame.Surface( global_.screen.get_size() )
	global_.background = global_.background.convert()
	global_.background.fill( ( 250, 250, 250 ) )

	global_.screen.blit( global_.background, (0, 0) )
	pygame.display.flip()

def tick():
	# this is what the testy code did:
	get_player_updates()

	for user, p in global_.players.iteritems():
		if not p == None:
			p.redraw( global_.screen )
#			print 'drawing', user
		else:
			print "Error with ", user
	pass

def get_player_updates():
	data, addr = network_comms.read()

	if len( data ) == 0:
		return
	
	EDIDecoder( edicomm.decode( data ), addr )
	return

def EDIDecoder( EDI, addr ):
	
	EDIargs = EDI
	
#	print EDIargs
	
	if   EDIargs[0] == 'LAG':
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
	elif EDIargs[0] == 'USI':
		print EDIargs
		p = findPlayerByName( global_.username )
		if not p == None:
			print 'WTF, we got 2 ID\'s'
			p.id = int( EDIargs[1] )
		else:
			global_.plr = Player( global_.username )
			global_.plr.position[0] = 0
			global_.plr.position[1] = 0
			global_.plr.id = EDIargs[ 1 ]
			global_.players[ EDIargs[ 1 ] ] = plr
	elif EDIargs[0] == 'USJ':
		p = findPlayerByName( EDIargs[ 1 ] )
		if not p == None:
			del players[ p.id ]
		p = Player( EDIargs[1] )
		p.position[0] = 0
		p.position[1] = 0
		p.id = EDIargs[2]
		global_.players[ EDIargs[2] ] = p
	elif EDIargs[0] == 'USM':
		p = global_.players[ EDIargs[1] ]
		if not p == None:
			p.position[0] = int( EDIargs[2] )
			p.position[1] = int( EDIargs[3] )
	else:
		pass
#		print 'Errrr...'
	return