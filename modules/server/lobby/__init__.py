""" Lobby state handling for Guns!, the tank game.

Runs in its own thread alongside the main thread.

"""

import lobby_thread, messages

def start_server():
	lobby_thread.server.start()

	print 'Lobby server thread started.'

def timer_tick():
	messages.process_queue()
