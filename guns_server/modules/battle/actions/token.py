import edicomm
from .. import player

def process(ediparts, addr):
	if len(ediparts) != 2:
		raise edicomm.EDIException(99, 'Wrong argument count!')

	# TODO: Validation!
	token = ediparts[1]

	print 'Got new player with token', token

	if token not in player.tokens:
		player.tokens.append(token)

	newid = player.tokens.index(token)

	p = player.by_token(token)

	if not p:
		p = player.new_player(newid, token)

	p.addr = addr
	p.enqueue(edicomm.encode('UID', p.id))

	print 'Player (token:', token, ') got id', p.id
