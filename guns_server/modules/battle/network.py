import edicomm
import actions, player
import constants

import socket, select

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(constants.listen_addr)

def check_input():
	while True:
		socks = select.select([sock], [], [], 0)

		if len(socks[0]) == 0:
			return
		
		try:
			data, addr = sock.recvfrom(2048)
			data = data.strip()
			print 'got data: ', data, 'from', addr
	
			try:
				actions.dispatch(edicomm.decode(data), addr)
			except edicomm.EDIException as e:
				sock.sendto(edicomm.encode('ERR', str(e.id), e.msg), addr)
		except:
			pass
			

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
