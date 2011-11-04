""" Auth functions for the Guns! server.

More docstringy stuff here.

"""

import sys, os, base64
from modules.server import constants
from modules import rsa
import hashlib


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

	key = rsa.PrivateKey.load_pkcs1(s)
	pub = rsa.PublicKey(key.n, key.e)

	print 'Imported server\'s private key.'

def player_token(name):
	hash = hashlib.md5(name).digest()
	return base64.encodestring(hash).rstrip()

pass
