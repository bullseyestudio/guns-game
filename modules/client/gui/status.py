from modules.client.gui import common
from modules.pgu import gui as pgui

wid = common.screen.get_width()
hgt = common.screen.get_height()

t = pgui.Table(width=wid, height=hgt)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt/2) - (3*40)))

t.tr()
l1 = pgui.Label('')
t.td(l1)

t.tr()
l2 = pgui.Label('')
t.td(l2)

t.tr()
t.td(pgui.Spacer(width=150, height=int(hgt/2) - (3*40) - 80))

t.tr()
cancel_btn = pgui.Button('Cancel', height=40)
cancel_btn.connect(pgui.CLICK, common.show_mainmenu)
t.td(cancel_btn)

t.tr()
t.td(pgui.Spacer(width=150, height=80))
