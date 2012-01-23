""" Auth functions for the Guns! server.

More docstringy stuff here.

"""

import sys, os, base64
from modules.server import config
from modules import rsa
import hashlib


key = None
pub = None

def init():
	global key, pub

	pk_path = config.cp.get('auth', 'private_key_path')

	if not os.access(pk_path, os.R_OK):
		print 'Unable to read server private key at {0}. Running as anonymous server.'.format(pk_path)
		config.cp.set('auth', 'server_name', 'noname')
		return

	fh = open(pk_path, 'rb')
	s = ''.join(fh.readlines())
	fh.close()

	key = rsa.PrivateKey.load_pkcs1(s)
	pub = rsa.PublicKey(key.n, key.e)

	print 'Imported server\'s private key.'

def player_token(name):
	hash = hashlib.md5(name).digest()
	return base64.encodestring(hash).rstrip()

pass
