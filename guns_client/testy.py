#!/usr/bin/env python

import sys
import socket, select

if len(sys.argv) < 3:
	sys.stderr.write('Usage: testy.py username server\r\n')
	sys.exit(2)

username = sys.argv[1]
host = sys.argv[2]
plr = None

try:
	import pygame
	from pygame.locals import *
except ImportError, err:
	sys.stderr.write('This application absolutely requires pygame. Sorry.\r\n')
	sys.exit(1)

# Initialise screen
pygame.init()
screen = pygame.display.set_mode((1024, 576))
pygame.display.set_caption('Basic Pygame program')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((host, 45005))

class Player:
	font = pygame.font.Font(None, 36)

	def __init__(self, newname):
		self.name = newname
		self.position = [ 0, 0 ]
		self.textcolor = ( 10, 10, 10 )
		self.text = self.font.render( self.name, 1, self.textcolor )
		self.textpos = self.text.get_rect()

	def redraw(self, screen):
		screen.blit(background, self.textpos, self.textpos)

		self.textpos.centerx = self.position[0]
		self.textpos.centery = self.position[1]

		screen.blit(self.text, self.textpos)


# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

pygame.time.set_timer(USEREVENT+1, 20)
velocity = [0, 0]

players = {}

def findPlayerByName( name ):
	ret = None
	for id, p in players.iteritems():
		if p.name == name:
			ret = p
	return ret

def EDIDecoder( EDI, addr ):
	global plr
	
	EDIargs = EDI.split( ' ' )
	
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
		p = findPlayerByName( username )
		if not p == None:
			print 'WTF, we got 2 ID\'s'
			p.id = int( EDIargs[1] )
		else:
			plr = Player(username)
			plr.position[0] = 0
			plr.position[1] = 0
			plr.id = EDIargs[1]
			players[EDIargs[1]] = plr
	elif EDIargs[0] == 'USJ':
		p = findPlayerByName( EDIargs[1] )
		if not p == None:
			del players[ p.id ]
		p = Player( EDIargs[1] )
		p.position[0] = 0
		p.position[1] = 0
		p.id = EDIargs[2]
		players[ EDIargs[2] ] = p
	elif EDIargs[0] == 'USM':
		p = players[ EDIargs[1] ]
		if not p == None:
			p.position[0] = int( EDIargs[2] )
			p.position[1] = int( EDIargs[3] )
	else:
		pass
#		print 'Errrr...'
	return

def get_player_updates():
	socks = select.select([sock], [], [], 0)

	if len(socks[0]) == 0:
		return
	
	data, addr = sock.recvfrom(1500)
	
	EDIDecoder( data, addr )
	return

#	lines = data.split('\r\n')

#	for l in lines:
#		print 'processing line:', l
#		user, xpos, ypos = l.split(' ')

#		if user in players:
#			p = players[user]

#			p.position[0] = int(xpos)
#			p.position[1] = int(ypos)
#		else:
#			p = Player(user)

#			p.position[0] = int(xpos)
#			p.position[1] = int(ypos)

#			players[user] = p

# sock.send('{0} 0 0\r\n'.format(username))
sock.send( 'USA {0}\r\n'.format( username ) )

# Event loop
while 1:
	for event in pygame.event.get():
		if event.type == USEREVENT+1:
			get_player_updates()

			for user, p in players.iteritems():
				p.redraw(screen)
				print 'drawing', user
		elif event.type == KEYDOWN:

			if event.key == K_s:
				velocity[1] = 5
			elif event.key == K_w:
				velocity[1] = -5
			elif event.key == K_a:
				velocity[0] = -5
			elif event.key == K_d:
				velocity[0] = 5
			elif event.key == K_z:
				velocity = [0, 0]
			elif event.key == K_x:
				print players.items()
#				sock.send('USC 1 255,0,0')
#			sock.send('{0} {1[0]} {1[1]}\r\n'.format(username, velocity))
			sock.send('USP {0} {1[0]} {1[1]}\r\n'.format(plr.id, velocity))
			
		elif event.type == KEYUP:
			if event.key in [K_s, K_w, K_a, K_d]:
				velocity = [0, 0]
#			sock.send('{0} {1[0]} {1[1]}\r\n'.format(username, velocity))
			sock.send('USP {0} {1[0]} {1[1]}\r\n'.format(findPlayerByName(username).id, velocity))

		elif event.type == QUIT:
			sock.send('USD {0}'.format(plr.id))
			sock.close()
			sys.exit(0)

	pygame.display.flip()
