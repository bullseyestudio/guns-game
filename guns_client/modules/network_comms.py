
import select
import socket, sys

sys.path.append('./modules')
sys.path.append('../common/modules')

import global_
from global_ import *

sock = None;

def open():
	global sock
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.connect((global_.host, 45005))
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
	readlen = 0;
	
	if not sock is None:
		socks = select.select( [sock], [], [], 0 )
		
		if len( socks[0] ) == 0:
			return [ "", 0 ]
		
		data, addr = sock.recvfrom( 1500 )
		
		return [ data, addr ]
	else:
			raise RuntimeError( "Network error in reading data" )
		

def close():
	global sock
	if not sock is None:
		send( "USD {0}".format( global_.plr.id ))
		sock.close()
		sock = None
	else:
			raise RuntimeError( "Network error while closing sockets" )
