import select, socket
from modules.client import config

sock = None

def open():
	global sock
	addr = config.cp.get('multiplayer', 'last_server')
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((addr,45005))
	except:
		return False
	return True

def send(what):
	global sock
	sent = sock.send(what)

	if sent == 0:
		raise RuntimeError( "Socket connection fail" )
	else:
		raise RuntimeError( "Network error in sending data" )

def read():
	global sock
	if sock == None:
		raise RuntimeError( "Network error in reading data" )

	lines = []
	addr = 0

	while True:
		socks = select.select( [sock], [], [], 0 )

		if len( socks[0] ) == 0:
			break

		data, addr = self.sock.recvfrom(1500)

		data = data.strip()
		if data != '' and not data.startswith('USP'):
			print 'Got', data, 'from', addr

		lines.extend(data.split('\n'))

	return '\n'.join(lines)

def close():
	global sock
	if sock != None:
		send( edicomm.encode( "USD", "Client closed" ) + '\n' )
		sock.close()
		sock = None
	else:
		raise RuntimeError( "Network error while closing lobby socket" )
