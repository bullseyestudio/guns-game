
from modules.client.gui import common
from modules.pgu import gui

wid = common.screen.get_width()
hgt = common.screen.get_height()

t = gui.Table(width=wid, height=hgt)

t.tr()
t.td(gui.Image('data/GunsLogo.png', valign=-1), height=int(hgt/2))

t.tr()
t.td(gui.Button('Multiplayer', width=150, height=30))

t.tr()
t.td(gui.Button('Options', width=150, height=30))

t.tr()
b = gui.Button('Quit', width=150, height=30)
t.td(b)

t.tr()
t.td(gui.Spacer(width=150, height=int(hgt/2) - (3 * 40)))
