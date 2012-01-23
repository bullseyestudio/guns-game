import ConfigParser
import os, io

default_config = """
[core]
listen_ip: 0.0.0.0
listen_port: 45005

[waypoints]
player_wp_fmtstring: wp_{{p.name}}
min_player_wpid: 256

[auth]
server_name: noname
private_key_path: {dotpath}/server.key
""".format(dotpath = os.path.expanduser('~/.guns'))

cp = ConfigParser.RawConfigParser()
conf_path = os.path.expanduser('~/.guns/server.cfg')

def read_config():
	global default_config, cp, conf_path

	cp.readfp(io.BytesIO(default_config))
	print 'Read default configuration.'

	read_configs = cp.read(conf_path)
	for f in read_configs:
		print 'Read configuration from {0}'.format(f)

def write_config():
	global cp, conf_path

	if not os.path.exists(os.path.expanduser('~/.guns')):
		os.makedirs(os.path.expanduser('~/.guns'))

	with open(conf_path, 'wb') as fh:
		cp.write(fh)
