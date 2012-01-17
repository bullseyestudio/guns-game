from modules import edicomm
from modules.server import config
import actions, player

import socket, select

sock = None

def listen():
	global sock

	listen_addr = (config.cp.get('core', 'listen_ip'), config.cp.getint('core', 'listen_port'))

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(listen_addr)

def check_input():
	global sock

	while True: # breakout by return a few lines below
		socks = select.select([sock], [], [], 0)

		if len(socks[0]) == 0:
			return

		try:
			data, addr = sock.recvfrom(1500)
		except socket.error:
			# Swallowing socket.error 10054 because UDP shouldn't fucking care!
			continue

		data = data.strip()
		if data != '':
			print 'got data: ', data, 'from', addr

			try:
				actions.dispatch(edicomm.decode(data), addr)
			except edicomm.EDIException as e:
				sock.sendto(edicomm.encode('ERR', str(e.id), e.msg), addr)


def to_ready(text):
	""" Send text to all players who are ready """
	for p in player.all:
		if p.ready:
			p.enqueue(text)

def to_observing(p, text):
	""" Send text to players who .can_see(p) """
	for obs in player.all:
		if obs.can_see(p):
			obs.enqueue(text)

def to_observing_at(coords, text):
	""" Send text to players who .can_see_at(coords) """
	for obs in player.all:
		if obs.can_see_at(coords):
			obs.enqueue(text)
