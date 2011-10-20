from modules import edicomm
from .. import player, waypoint, network

def process(ediparts, p):
	if len(ediparts) != 2:
		raise edicomm.EDIException(99, 'Wrong argument count!')

	# TODO: Validation!
	newname = ediparts[1]

	print 'Player', p.id, 'sets name to', newname, 'from', p.name

	p.name = newname

	network.to_ready(edicomm.encode('USN', p.id, p.name))

	p.ready = True

	nickmap = [edicomm.encode('USN', pl.id, pl.name) for pl in player.all if pl.ready]
	wpt_map = [edicomm.encode('WPT', wp.id, wp.position, wp.title, wp.owner) for wp in waypoint.all]

	p.enqueue('\n'.join(nickmap + wpt_map))
