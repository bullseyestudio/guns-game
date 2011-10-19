from .. import player
import edicomm

def dispatch(ediparts, addr):
	ediparts[0] = ediparts[0].upper() # for easier case-insensitive comparison
	p = player.by_addr(addr)

	if (not p) and (ediparts[0] != 'UST'):
		raise edicomm.EDIException(100, 'Please re-authenticate!')

	if ediparts[0] == 'UST':
		import token
		token.process(ediparts, addr)
	elif ediparts[0] == 'USN':
		import nick
		nick.process(ediparts, p)
	elif ediparts[0] == 'USD':
		import disconnect
		disconnect.process(ediparts, p)
	elif ediparts[0] == 'USV':
		import velocity
		velocity.process(ediparts, p)
	elif ediparts[0] == 'USF':
		import fire
		fire.process(ediparts, p)
	elif ediparts[0] == 'USR':
		import viewport
		viewport.process(ediparts, p)
	elif ediparts[0] == 'USZ':
		import zoom
		zoom.process(ediparts, p)
	elif ediparts[0] == 'WPT':
		import waypoint
		waypoint.process(ediparts, p)
