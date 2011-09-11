#!/usr/bin/env python

import sys
import atexit

try:
	import pyreadline as readline
except ImportError:
	try:
		import readline
	except ImportError:
		sys.stderr.write('Cannot import libreadline. You\'ll have a pretty crippled command line. Sorry.\n')


sys.path.append('./modules')
sys.path.append('../common/modules')

import edicomm
import physim

import lobby
import battle
import auth

