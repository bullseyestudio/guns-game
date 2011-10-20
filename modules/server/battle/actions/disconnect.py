def process(ediparts, p):
	from .... import edicomm
	from .. import network

	print 'Player', p.name, 'disconnects'

	p.ready = False

	reason = 'Unknown reason'
	if len(ediparts) >= 2:
		reason = ediparts[1]

	network.to_ready(edicomm.encode('USD', p.id, reason))
