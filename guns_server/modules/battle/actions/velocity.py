import edicomm

def process(ediparts, p):
	if len(ediparts) != 2:
		raise edicomm.EDIException(99, 'Wrong argument count!')

	p.velocity = [int(x) for x in ediparts[1]]

	print 'Player', p.name, 'velocity change:', p.velocity
