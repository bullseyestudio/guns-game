import os, io, ConfigParser
from pygame import locals as pgl

TIMER_EVENT = pgl.USEREVENT + 8

default_config = """
[multiplayer]
last_nick:
last_server:

[auth]
canonical_name: nobody
key_path: ~/.guns/client.key

[keys]
forward: {pgl.K_w}
reverse: {pgl.K_s}
turn_left: {pgl.K_a}
turn_right: {pgl.K_d}
zoom_in: {pgl.K_KP_PLUS}
zoom_out: {pgl.K_KP_MINUS}

[mouse]
rmb: wp
lmb: fire
wheel_down: zoom_out
wheel_up: zoom_in

[window]
xpos: 0
ypos: 0
width: 1024
height: 576
"""

default_config = default_config.format(pgl=pgl)
conf_path = os.path.expanduser('~/.guns/client.cfg')
cp = ConfigParser.RawConfigParser()

def read_config():
	global default_config, cp, conf_path

	cp.readfp(io.BytesIO(default_config))

	read_config = cp.read(conf_path)

def write_config():
	global cp, conf_path

	if not os.path.exists(os.path.expanduser('~/.guns/')):
		os.makedirs(os.path.expanduser('~/.guns'))

	with open(conf_path, 'wb') as fh:
		cp.write(fh)
