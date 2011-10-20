""" Battle state handling for Guns!, the tank game. """
import network, player

def timer_tick():
	network.check_input()
	player.move_all()
	player.xmit_all()

