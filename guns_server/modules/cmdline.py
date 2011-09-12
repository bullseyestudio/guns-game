
"""Provides the server command line implementation for Guns!, the tank game.

Designed to work in its own thread.

"""

import sys
import threading
import Queue

try:
	import pyreadline as readline
except ImportError:
	try:
		import readline
	except ImportError:
		sys.stderr.write('Cannot import readline. You\'ll have a pretty crippled command line. Sorry.\n')

class GunsCommandLine(threading.Thread):
	def __init__(self, queue, condition):
		threading.Thread.__init__(self)
		self.queue = queue
		self.condition = condition

	def run(self):
		self.condition.acquire()
		while True:
			s = raw_input('> ')
			self.queue.put(s)
			self.condition.wait()


class cmdline:
	def __init__(self):
		self.q = Queue.Queue()
		self.c = threading.Condition()

		self.t = GunsCommandLine(self.q, self.c)
		self.t.setDaemon(True)

		self.commands = {}

	def add_command(self, str, fn):
		self.commands[str] = fn

	def start_listener(self):
		self.t.start()

	def handle_command(self):
		cmd = self.q.get()

		for str in self.commands.keys():
			if cmd[0:len(str)].lower() == str.lower():
				self.commands[str](cmd)

		self.c.acquire()
		self.c.notify_all()
		self.c.release()
