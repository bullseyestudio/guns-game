from modules.client.gui import common
from modules.pgu import gui as pgui
from modules.client import config

def savebtn_handler():
	global input_user

	config.cp.set('auth', 'canonical_name', input_user.value)
	common.show_mainmenu()

wid = common.screen.get_width()
hgt = common.screen.get_height()

t = pgui.Table(width=wid, height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=80), colspan=2)

t.tr()
t.td(pgui.Label('Guns-game.com username', height=30))
input_user = pgui.Input(value=config.cp.get('auth', 'canonical_name'))
t.td(input_user)

t.tr()
t.td(pgui.Label('More options later...', height=30), colspan=2)

t.tr()
t.td(pgui.Spacer(width=150, height=hgt - (2 * 80) - (3 * 40)), colspan=2)

t.tr()
backbtn = pgui.Button('Back to Main Menu', width=150, height=30)
backbtn.connect(pgui.CLICK, common.show_mainmenu)
t.td(backbtn)
savebtn = pgui.Button('Save Settings', width=150, height=30)
savebtn.connect(pgui.CLICK, savebtn_handler)
t.td(savebtn)

t.tr()
t.td(pgui.Label('(without saving)'))
t.td(pgui.Label('(and back to main menu)'))

t.tr()
t.td(pgui.Spacer(width=150, height=40), colspan=2)
