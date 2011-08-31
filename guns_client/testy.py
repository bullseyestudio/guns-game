#!/usr/bin/env python

import sys
import socket, select

if len(sys.argv) < 2:
	sys.stderr.write('Usage: testy.py username\r\n')
	sys.exit(2)

username = sys.argv[1]

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
sock.connect(('hermes', 45005))

class Player:
	font = pygame.font.Font(None, 36)

	def __init__(self, newname):
		self.name = newname
		self.position = [0,0]
		self.text = self.font.render(self.name, 1, (10, 10, 10))
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

def get_player_updates():
	socks = select.select([sock], [], [], 0)

	if len(socks[0]) == 0:
		return

	data, addr = sock.recvfrom(1500)
	data = data.strip()

	lines = data.split('\r\n')

	for l in lines:
		print 'processing line:', l
		user, xpos, ypos = l.split(' ')

		if user in players:
			p = players[user]

			p.position[0] = int(xpos)
			p.position[1] = int(ypos)
		else:
			p = Player(user)

			p.position[0] = int(xpos)
			p.position[1] = int(ypos)

			players[user] = p

# Event loop
while 1:
	for event in pygame.event.get():
		if event.type == USEREVENT+1:
			print 'something something'
			get_player_updates()

			for user, p in players.iteritems():
				p.redraw(screen)
				print 'drawing', user
		elif event.type == KEYDOWN:
			print 'something else'

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

			sock.send('{0} {1[0]} {1[1]}\r\n'.format(username, velocity))
		elif event.type == KEYUP:
			if event.key in [K_s, K_w, K_a, K_d]:
				velocity = [0, 0]

			sock.send('{0} {1[0]} {1[1]}\r\n'.format(username, velocity))

		elif event.type == QUIT:
			sock.close()
			sys.exit(0)

	pygame.display.flip()
