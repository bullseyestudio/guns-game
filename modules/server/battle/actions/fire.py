from modules import edicomm
from .. import network, locals, player

def process(ediparts, p):
	if len(ediparts) != 2:
		raise edicomm.EDIException(99, 'Wrong argument count!')

	desired_shot = [int(x) for x in ediparts[1]]

	network.to_observing_at(desired_shot, edicomm.encode('USF', p.id, desired_shot))

	# HACK: Quick and dirty "death" of player that gets shot
	for pl in player.all:
		if not pl.id == p.id and pl.contains( desired_shot ):
			pl.position = locals.spawn
			pl.velocity = [0,0]
