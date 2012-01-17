from modules.client.gui import common
from modules.pgu import gui as pgui
from modules.client import config

hgt = common.screen.get_height()
t = pgui.Table(width=common.screen.get_width(), height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=80), colspan=2)

t.tr()
t.td(pgui.Label('Server address:', height=30))
input_server = pgui.Input(value=config.cp.get('multiplayer', 'last_server'))
t.td(input_server)

t.tr()
t.td(pgui.Label('Your nickname on the server:', height=30))
input_nick = pgui.Input()
t.td(input_nick)

t.tr()
t.td(pgui.Spacer(width=150, height=hgt - (2 * 80) - (3 * 40)), colspan=2)

t.tr()
backbtn = pgui.Button('Back to Main Menu', width=150, height=30)
t.td(backbtn)
connectbtn = pgui.Button('Connect', width=150, height=30)
t.td(connectbtn)

t.tr()
t.td(pgui.Label('(without connecting)'))
t.td(pgui.Spacer(width=150, height=30))

t.tr()
t.td(pgui.Spacer(width=150, height=40), colspan=2)

initialized = False
def init():
	global initialized
	if initialized:
		return

	global backbtn, connectbtn

	backbtn.connect(pgui.CLICK, hide)
	connectbtn.connect(pgui.CLICK, connect)

	initialized = True


def connect():
	config.cp.set('multiplayer', 'last_nick', input_nick.value)
	config.cp.set('multiplayer', 'last_server', input_server.value)

	import status
	status.l1.value = 'Connecting to {0}...'.format(input_server.value)
	status.l2.value = '(or, we would if that functionality were complete)'
	status.show()

	# TODO: Hint to the lobby client that we want to start the connection process.
	# TODO: Also assign status.abort_callback to something that will abort that process.


def show():
	init()

	global input_nick
	nick = config.cp.get('multiplayer', 'last_nick')
	if nick == '':
		nick = config.cp.get('auth', 'canonical_name')
	input_nick.value = nick

	common.draw_background()
	common.pguapp.init(t, common.screen)

def hide():
	import mainmenu
	mainmenu.show()
