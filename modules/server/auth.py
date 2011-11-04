""" Auth functions for the Guns! server.

More docstringy stuff here.

"""

import sys, os, base64
from modules.server import constants

try:
	from Crypto.Hash import MD5
	from Crypto.PublicKey import RSA
	import Crypto.Random
except ImportError:
	sys.stderr.write('Sorry, this application absolutely requires pycrypto >= v2.2.\r\nTry sudo apt-get python-crypto, if you\'re on a deb-system.\r\n')
	sys.exit(1)

key = None
pub = None

def init():
	global key, pub

	if not os.access(constants.private_key_path, os.R_OK):
		sys.stderr.write(
			'Unable to read private server key at {0}. Please verify a key exists and start the server again.\r\n'
				.format(constants.private_key_path)
		)
		sys.exit(1)

	fh = open(constants.private_key_path, 'rb')
	s = ''.join(fh.readlines())
	fh.close()

	key = RSA.importKey(s)
	pub = key.publickey()

	print 'Imported server\'s private key.'

def player_token(name):
	hash = MD5.new(name)
	return hash.digest()

pass
