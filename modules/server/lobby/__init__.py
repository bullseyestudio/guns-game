""" Lobby state handling for Guns!, the tank game.

Runs in its own thread alongside the main thread.

"""

from modules.server import constants
import lobby_thread, player, messages

def start_server():
	lobby_thread.server.start()

	print 'Lobby server thread started.'

def timer_tick():
	messages.process_queue()
