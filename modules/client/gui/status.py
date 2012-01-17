from modules.client.gui import common
from modules.pgu import gui as pgui

# l1, l2, and abort_callback are designed to be tweaked by external forces:
# - l1 and l2's .value property can be set to change the displayed message
# - abort_callback should be set to a function to be called if user presses "cancel"

l1 = pgui.Label('One moment...')
l2 = pgui.Label('(if you see this for longer than a moment, something\'s probably gone wrong)')
abort_callback = None

hgt = common.screen.get_height()
t = pgui.Table(width=common.screen.get_width(), height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt/2) - (3*40)))

t.tr()
t.td(l1)

t.tr()
t.td(l2)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt/2) - (3*40) - 80))

t.tr()
cancel_btn = pgui.Button('Cancel', height=40)
t.td(cancel_btn)

t.tr()
t.td(pgui.Spacer(width=150, height=80))

initialized = False
def init():
	global initialized
	if initialized:
		return

	global cancel_btn
	cancel_btn.connect(pgui.CLICK, hide)

	initialized = True

def show():
	init()

	common.draw_background()
	common.pguapp.init(t, common.screen)

def hide():
	global l1, l2, abort_callback

	l1.value = 'Aborting...'
	l2.value = ''

	if abort_callback:
		abort_callback()

	abort_callback = None

	import mainmenu
	mainmenu.show()
