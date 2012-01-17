from modules.client.gui import common
from modules.pgu import gui as pgui
from modules.client import config

hgt = common.screen.get_height()
t = pgui.Table(width=common.screen.get_width(), height=hgt)

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
t.td(backbtn)
savebtn = pgui.Button('Save Settings', width=150, height=30)
t.td(savebtn)

t.tr()
t.td(pgui.Label('(without saving)'))
t.td(pgui.Label('(and back to main menu)'))

t.tr()
t.td(pgui.Spacer(width=150, height=40), colspan=2)

initialized = False
def init():
	global initialized
	if initialized:
		return

	global backbtn, savebtn

	backbtn.connect(pgui.CLICK, hide)
	savebtn.connect(pgui.CLICK, save_and_hide)

	initialized = True

def show():
	init()

	global input_user
	input_user = pgui.Input(value=config.cp.get('auth', 'canonical_name'))

	common.draw_background()
	common.pguapp.init(t, common.screen)

def hide():
	import mainmenu
	mainmenu.show()

def save_and_hide():
	config.cp.set('auth', 'canonical_name', input_user.value)
	# TODO: Save the rest of the config settings

	hide()
