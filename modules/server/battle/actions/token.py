from modules import edicomm
from .. import player, waypoint, network

def process(ediparts, addr):
	if len(ediparts) != 2:
		raise edicomm.EDIException(99, 'Wrong argument count!')

	# TODO: Validation!
	token = ediparts[1]

	print 'Got new player with token', token

	if token not in player.tokens:
		print 'token',token,'is not in player.tokens!'
		raise edicomm.EDIException(100, 'Please re-authenticate!')

	p = player.by_token( token )

	if not p:
		print 'player could not be found from token',token
		raise edicomm.EDIException(100, 'Please re-authenticate!')

	p.addr = addr
	p.ready = True

	wpt_map = [edicomm.encode('WPT', wp.id, wp.position, wp.title, wp.owner) for wp in waypoint.all]

	p.enqueue( '\n'.join(wpt_map) )

	print 'Player (token:', token, ', username:', p.name, ', address: ', addr, ') joined!'
