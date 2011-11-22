from modules.client.gui import common
from modules.pgu import gui as pgui
from modules.client import config

def connect_handler():
	global input_nick, input_server

	config.cp.set('multiplayer', 'last_nick', input_nick.value)
	config.cp.set('multiplayer', 'last_server', input_server.value)
	common.show_status()

wid = common.screen.get_width()
hgt = common.screen.get_height()

t = pgui.Table(width=wid, height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=80), colspan=2)

t.tr()
t.td(pgui.Label('Server address:', height=30))
input_server = pgui.Input(value=config.cp.get('multiplayer', 'last_server'))
t.td(input_server)

t.tr()
t.td(pgui.Label('Your nickname on the server:', height=30))
nick = config.cp.get('multiplayer', 'last_nick')
if nick == '':
	nick = config.cp.get('auth', 'canonical_name')
input_nick = pgui.Input(value = nick)
t.td(input_nick)

t.tr()
t.td(pgui.Spacer(width=150, height=hgt - (2 * 80) - (3 * 40)), colspan=2)

t.tr()
backbtn = pgui.Button('Back to Main Menu', width=150, height=30)
backbtn.connect(pgui.CLICK, common.show_mainmenu)
t.td(backbtn)
connectbtn = pgui.Button('Connect', width=150, height=30)
connectbtn.connect(pgui.CLICK, connect_handler)
t.td(connectbtn)

t.tr()
t.td(pgui.Label('(without connecting)'))
t.td(pgui.Spacer(width=150, height=30))

t.tr()
t.td(pgui.Spacer(width=150, height=40), colspan=2)
