
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
		self.finished = False

	def run(self):
		self.condition.acquire()
		while not self.finished:
			s = raw_input('')
			self.queue.put(s)
			self.condition.wait()


class cmdline:
	def __init__(self):
		self.q = Queue.Queue()
		self.c = threading.Condition()

		self.t = GunsCommandLine(self.q, self.c)

		self.commands = {}

	def post_quit(self):
		self.t.finished = True

	def add_command(self, str, fn):
		self.commands[str] = fn

	def start_listener(self):
		self.t.start()

	def handle_command(self):
		if(self.q.empty()):
			return

		cline = self.q.get()
		cmd = cline.split(' ', 1)[0]

		found_cmd = None

		for k in self.commands.keys():
			if cmd.lower() == k.lower(): #exact match!
				found_cmd = self.commands[k]
				break
			elif k.lower().startswith(cmd.lower()): #partial match
				if found_cmd != None:
					print 'Ambiguous command! Try a few more letters.'
					found_cmd = None
					break
				else:
					found_cmd = self.commands[k]

		if found_cmd == None:
			print 'Couldn\'t find a command with that prefix. Try "help"'
		else:
			found_cmd(cline, self)

		self.c.acquire()
		self.c.notify_all()
		self.c.release()
