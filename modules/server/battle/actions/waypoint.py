from modules import edicomm
from modules.server import constants
from .. import waypoint, network

def process(ediparts, p):
	if len(ediparts) == 2: # Player wants waypoint set: WPT x,y
		wpid = constants.min_player_wpid + p.id
		wppos = [int(x) for x in ediparts[1]]
		wptitle = constants.player_wp_fmtstring.format(p=p)

		wp = waypoint.by_id(wpid)
		if not wp:
			wp = waypoint.Waypoint(wpid, wppos, wptitle)
			waypoint.all.append(wp)

		wp.owner = p.id

		network.to_ready(edicomm.encode('WPT', wpid, wppos, wptitle, p.id))
	elif len(ediparts) == 1: # Player wants waypoint deleted
		wpid = constants.min_player_wpid + p.id

		wp = waypoint.by_id(wpid)
		if wp:
			waypoint.all.remove(wp)

		network.to_ready(edicomm.encode('WPT', wpid))
	else:
		print 'Malformed WPT: {0}'.format( edicomm.encode(ediparts) )
		raise EDIException(99, 'Wrong argument count!')
