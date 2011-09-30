
"""Battle state handling for Guns!, the tank game.

"""

import socket, select
import edicomm

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 45005))

width = 1024
height = 576

class Player:
	def __init__(self, id, token):
		self.velocity = [0,0]
		self.position = [512,384]
		self.addr = None
		self.name = ''
		self.id = id
		self.token = token

players = {}
to_all = []

class EDIException(Exception):
	def __init__(self, id, msg):
		Exception.__init__(self)
		self.id = id
		self.msg = msg

def player_by_addr(addr):
	for i, p in players.iteritems():
		if p.addr == addr:
			return p

def act_on_edidata(ediparts, addr):
	global to_all
	ediparts[0] = ediparts[0].upper()

	if ediparts[0] == 'UST':
		if len(ediparts) != 2:
			raise EDIException(99, 'Wrong argument count!')

		print 'Got new player with token', ediparts[1]

		p = Player(len(players) + 1, ediparts[1])
		p.addr = addr
		players[p.id] = p

		print 'Player (token:', ediparts[1], ') got id', p.id
		sock.sendto(edicomm.encode(['UID', str(p.id)]), addr)
		return
	elif ediparts[0] == 'USN':
		if len(ediparts) != 2:
			raise EDIException(99, 'Wrong argument count!')

		p = player_by_addr(addr)

		if p == None:
			raise EDIException(100, 'Please re-authenticate')

		print 'Player', p.id, 'sets name to', ediparts[1], 'from', p.name

		p.name = ediparts[1]

		to_all.append(edicomm.encode(('USN', str(p.id), p.name)))
	elif ediparts[0] == 'USD':
		p = player_by_addr(addr)

		if p == None:
			raise EDIException(100, 'Please re-authenticate')

		print 'Player', p.name, 'disconnects'

		del players[p.id]
		to_all.append(edicomm.encode(('USD', str(p.id))))

def check_for_playerinput():
	socks = select.select([sock], [], [], 0)

	if len(socks[0]) == 0:
		return

	data, addr = sock.recvfrom(1500)
	data = data.strip()
	print 'got data: ', data, 'from', addr

	try:
		act_on_edidata(edicomm.decode(data), addr)
	except EDIException as e:
		sock.sendto(edicomm.encode(['ERR', str(e.id), e.msg]), addr)

def move_players():
	return
	#for user, p in players.iteritems():
	#	p.position[0] += int(p.velocity[0])
	#	p.position[1] += int(p.velocity[1])
	#
	#	if p.position[0] < 0 or p.position[0] > width:
	#		p.velocity[0] = -p.velocity[0]
	#	if p.position[1] < 0 or p.position[1] > height:
	#		p.velocity[1] = -p.velocity[1]

def tell_players():
	global to_all
	if len(to_all) < 1:
		return

	data = '\n'.join(to_all)
	to_all = []

	for uid, p in players.iteritems():
		sock.sendto(data, p.addr)


def timer_tick():
	check_for_playerinput()
	move_players()
	tell_players()
