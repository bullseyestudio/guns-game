from modules import edicomm

def process(ediparts, p):
	if len(ediparts) != 2:
		raise edicomm.EDIException(99, 'Wrong argument count!')

	p.viewport = [int(x) for x in ediparts[1]]
