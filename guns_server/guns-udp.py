#!/usr/bin/env python

import os, sys
import socket, select

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 45005))

width = 1024
height = 576

class Player:
	def __init__(self):
		self.velocity = [0,0]
		self.position = [0,0]
		self.addr = None
		self.name = ''

players = {}

def check_for_playerinput():
	socks = select.select([sock], [], [], 0)

	if len(socks[0]) == 0:
		return

	data, addr = sock.recvfrom(1500)
	data = data.strip()
	print 'got data: ', data, 'from', addr

	data_parts = data.split(' ')
	if len(data_parts) == 2:
		user, command = data_parts
		if user in players: del players[user]
		return
	elif len(data_parts) == 3:
		user, xvel, yvel = data_parts

	if user in players:
		p = players[user]

		print 'updating velocity for', p

		p.velocity[0] = int(xvel)
		p.velocity[1] = int(yvel)
		p.addr = addr
	else:
		p = Player()
		p.velocity[0] = int(xvel)
		p.velocity[1] = int(yvel)
		p.name = user
		p.addr = addr
		players[user] = p

def move_players():
	for user, p in players.iteritems():
		p.position[0] += int(p.velocity[0])
		p.position[1] += int(p.velocity[1])

		if p.position[0] < 0 or p.position[0] > width:
			p.velocity[0] = -p.velocity[0]
		if p.position[1] < 0 or p.position[1] > height:
			p.velocity[1] = -p.velocity[1]

def tell_players():
	data = ''

	for user, p in players.iteritems():
		data += '{0} {1[0]} {1[1]}\r\n'.format(p.name, p.position)

	for user, p in players.iteritems():
		sock.sendto(data, p.addr)

def timer_tick():
	check_for_playerinput()
	move_players()
	tell_players()

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from pygame.locals import *

pygame.display.init()
screen = pygame.display.set_mode((1,1))

pygame.time.set_timer(USEREVENT+1, 20)

while 1:
	for event in pygame.event.get():
		if event.type == USEREVENT+1:
			timer_tick()
		elif (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_q):
			sys.exit(0)
