
import select, socket

import constants
import edicomm

sock = None;

def open():
	global sock
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.connect((constants.host, 45005))
	if sock is None:
		raise RuntimeError( "Unable to connect to the remote host" )

def send( what ):
	global sock
	if not sock is None:
		sent = sock.send( what )

		if sent == 0:
			raise RuntimeError( "Socket connection fail" )
	else:
			raise RuntimeError( "Network error in sending data" )


def read( ):
	global sock

	if sock is None:
		raise RuntimeError( "Network error in reading data" )

	lines = []
	addr = 0

	while True:
		socks = select.select( [sock], [], [], 0 )

		if len( socks[0] ) == 0:
			break

		data, addr = sock.recvfrom( 1500 )

		if not data.startswith('USP'):
			print 'Got', data, 'from', addr

		lines.extend(data.split('\n'))

	return '\n'.join(lines)


def close():
	global sock
	if not sock is None:
		send( edicomm.encode( "USD", "Client closed" ) )
		sock.close()
		sock = None
	else:
		raise RuntimeError( "Network error while closing sockets" )
