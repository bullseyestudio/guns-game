from modules import edicomm
from modules.client import protocol, config
from modules.client.gui import common as gui
from modules.client.gui import lobby as lobbygui
import network

def start():
	if network.open() == True:
		gui.show_lobby()
	else:
		gui.show_mpmenu()


def tick(ev):
	if ev.type != config.TIMER_EVENT:
		return

	updates = network.read()
	if len( updates ) == 0:
		return

	dlines = data.split( "\n" )
	for i in dlines:
		handle( edicomm.decode( i ) )

def handle(cmd):
	if(cmd[0] == protocol.USERNAME):
		print 'Recieved {0} FOR {1}: {2}'.format(protocol.USERNAME,cmd[1],cmd[2])
	elif(cmd[0] == protocol.ID):
		print 'Recieved {0}: {1}'.format(protocol.USERNAME,cmd[1])
	else:
		pass

