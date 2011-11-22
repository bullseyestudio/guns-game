import ConfigParser
import os

default_config = {
	'core':
		{
			'listen_ip': '0.0.0.0',
			'listen_port': 45005
		},
	'waypoints':
		{
			'player_wp_fmtstring': 'wp_{p.name}',
			'min_player_wpid': 256
		},
	'auth':
		{
			'server_name': 'hermes',
			'private_key_path': 'data/server.key'
		}
	}

print 'Set up default configuration.'

cp = ConfigParser.RawConfigParser(default_config)
read_configs = cp.read(['data/server.cfg', os.path.expanduser('~/.guns/server.cfg')])

for f in read_configs:
	print 'Read configuration from {0}'.format(f)

listen_ip = cp.get('core', 'listen_ip')
listen_port = cp.getint('core', 'listen_port')
listen_addr = (listen_ip, listen_port)

player_wp_fmtstring = cp.get('waypoints', 'player_wp_fmtstring')
min_player_wpid = cp.getint('waypoints', 'min_player_wpid')

server_name = cp.get('auth', 'server_name')
private_key_path = cp.get('auth', 'private_key_path')
