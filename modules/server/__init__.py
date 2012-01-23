import pygame
import signal

from modules.server import cmdline

quitting = False
cl = cmdline.cmdline()

def init():
	print 'Server init begins.'

	pygame.display.init()
	screen = pygame.display.set_mode((1,1))
	print 'Pygame display set up.'

	from modules.server import config
	config.read_config()
	print 'Configuration ready.'

	from modules.server import auth
	auth.init()
	print 'Auth module initialized.'

	from modules.server import lobby, battle
	lobby.start_server()
	battle.start_server()
	print 'Lobby and battle servers started.'

	global cl
	from modules.server import cmdhandlers
	for k, h in cmdhandlers.handlers.iteritems():
		cl.add_command(k, h)
	cl.start_listener()
	print 'Command-line listener listening.'

def timer_tick(elapsed):
	global cl

	lobby.timer_tick()
	battle.timer_tick()
	cl.handle_command()

def exit():
	cl.post_quit()
	config.write_config()
