#!/usr/bin/env python

import os, sys
import socket, select
from collections import deque

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 45005))

width = 1024
height = 576

class Player:
	plrCount = 0;
	def __init__(self):
		self.velocity = [0,0]
		self.position = [0,0]
		self.addr = None
		self.name = ''
		Player.plrCount += 1
		self.id = Player.plrCount
		self.moved = 0
		self.active = 0

players = {}

def findPlayerByAddr( addr ):
	ret = None
	for id, p in players.iteritems():
		if p.addr == addr:
			ret = p
	return ret

def findPlayerByName( name ):
	ret = None
	for id, p in players.iteritems():
		if p.name == name:
			ret = p
	return ret

def EDIDecoder( EDI, addr ):
	EDIargs = EDI.split( ' ' )
	
	print EDIargs
	
	if   EDIargs[0] == 'LAG':
		print 'Ping test, please.'
	elif EDIargs[0] == 'MSG':
		print 'Message to everyone.'
	elif EDIargs[0] == 'MST':
		print 'Message to team'
	elif EDIargs[0] == 'USA':
		print 'User \'{0}\' connected to the server.'.format( EDIargs[ 1 ] )
		p = findPlayerByName( EDIargs[1] )
		if not p == None:
			if p.active == 0:
				p.velocity[0] = 0
				p.velocity[1] = 0
				p.addr = addr
				p.active = 1
			else:
				print 'HACK ATTEMPT'
		else:
			p = Player()
			p.velocity[0] = 0
			p.velocity[1] = 0
			p.addr = addr
			p.name = EDIargs[ 1 ]
			p.active = 1
			players[ p.id ] = p
		data = 'USI {0}'.format( p.id )
		sock.sendto( data, addr )
		updatePlayers( p.id )
	elif EDIargs[0] == 'USC':
		print 'Hey I should be a different colour'
	elif EDIargs[0] == 'USD':
		print 'Rage quit'
		uid = int( EDIargs[1] )
		if uid in players:
			del players[uid]
	elif EDIargs[0] == 'USP':
		print 'I moved.'
		p = players[ int( EDIargs[1] ) ]
		p.velocity[0] = int( EDIargs[2] )
		p.velocity[1] = int( EDIargs[3] )
		
		if ( p.velocity[0] == 0 ) and ( p.velocity[1] == 0 ):
			p.moved = 0
			print '{0} stopped'.format( p.id )
		else:
			p.moved = 1
			print '{0} moving'.format( p.id )
	else:
		print 'Errrr...'
	return

def check_for_playerinput():
	socks = select.select([sock], [], [], 0)

	if len(socks[0]) == 0:
		return

	data, addr = sock.recvfrom(1500)
	data = data.strip()
	print 'got data: ', data, 'from', addr

	EDIDecoder( data, addr )

def move_players():
	for user, p in players.iteritems():
		p.position[0] += int(p.velocity[0])
		p.position[1] += int(p.velocity[1])

		if p.position[0] < 0 or p.position[0] > width:
			p.velocity[0] = -p.velocity[0]
		if p.position[1] < 0 or p.position[1] > height:
			p.velocity[1] = -p.velocity[1]

def tell_players():
	data = {}

	for uid, p in players.iteritems():
		if p.moved == 1:
			data[ uid ] = 'USM {0} {1[0]} {1[1]}'.format(uid, p.position)
			#p.moved = 0

	for uid, p in players.iteritems():
		for id, d in data.iteritems():
			sock.sendto(d, p.addr)
			print d

def updatePlayers( pid ):
	data = deque('')

	for uid, p in players.iteritems():
		if not p.id == pid:
			data.append( 'USJ {0} {1}'.format(p.name, uid) )
			data.append( 'USM {0} {1[0]} {1[1]}'.format(uid, p.position) )
	
	p = players[ pid ]
	for d in data:
		sock.sendto(d, p.addr)
		print d
	
	data.clear()
	
	data.append( 'USJ {0} {1}'.format(p.name, pid) )
	data.append( 'USM {0} {1[0]} {1[1]}'.format(pid, p.position) )

	for uid, p in players.iteritems():
		for d in data:
			sock.sendto(d, p.addr)
			print d

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
