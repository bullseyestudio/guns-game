""" Battle state handling for Guns!, the tank game. """
import network, player

def start_server():
	network.listen()

def timer_tick():
	network.check_input()
	player.move_all()
	player.xmit_all()
