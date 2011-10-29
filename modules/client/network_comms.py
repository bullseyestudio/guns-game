import select, socket

from modules import edicomm

import constants

battle = None
lobby = None

class NetComm():
	def __init__( self, socktype ):
		self.sock = None
		self.type = socktype


		if self.type == constants.socket_udp:
			protocol = socket.SOCK_DGRAM
		else:
			protocol = socket.SOCK_STREAM

		self.sock = socket.socket(socket.AF_INET, protocol)
		self.sock.connect((constants.host, 45005))
		if self.sock is None:
			raise RuntimeError( "Unable to connect to the remote host" )

	def send(self, what):
		if self.sock != None:
			sent = self.sock.send( what )

			if sent == 0:
				raise RuntimeError( "Socket connection fail" )
		else:
			raise RuntimeError( "Network error in sending data" )

	def read(self):
		if self.sock == None:
			raise RuntimeError( "Network error in reading data" )

		lines = []
		addr = 0

		while True:
			socks = select.select( [self.sock], [], [], 0 )

			if len( socks[0] ) == 0:
				break

			if self.type == constants.socket_udp:
				try:
					data, addr = self.sock.recvfrom(1500)
				except socket.error:
					# Swallowing socket.error 10054 because UDP shouldn't fucking care!
					continue
			else:
				data, addr = self.sock.recvfrom(1500)

			data = data.strip()
			if data != '' and not data.startswith('USP'):
				print 'Got', data, 'from', addr

			lines.extend(data.split('\n'))

		return '\n'.join(lines)

	def close(self):
		if self.sock != None:
			if self.type == constants.socket_udp:
				self.send( edicomm.encode( "USD", "Client closed" ) )
				self.sock.close()
				self.sock = None
			else:
				self.sock.close()
				self.sock = None
		else:
			raise RuntimeError( "Network error while closing sockets" )

def open():
	global battle, lobby
	battle = NetComm( constants.socket_udp )
	lobby = NetComm( constants.socket_tcp )