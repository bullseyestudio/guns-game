import Queue
import player
from modules import edicomm

queue = Queue.Queue();

def tick():
	if queue.empty() == False:
		handle_queue()

def handle_queue():
	instr = queue.get(False)
	EDIDecode( edicomm.decode( instr ) )
	queue.task_done()

def EDIDecode(instr):
	print instr
	if instr[0] == 'ECHO':
		print 'Lobby:',instr[1]
	elif instr[0] == 'USR':
		pid = int(instr[1])
		username = instr[2]
		token = instr[3]

		print 'Adding player',username,'(',pid,') with token',token

		player.tokens.append(token)
		p = player.by_token( token )

		if not p:
			p = player.Player(pid, token)
			p.name = username
			player.all.append(p)
		else:
			p.id = pid
			p.name = username
	elif instr[0] == 'USD':
		p = player.by_id(int(instr[1]))
		if p != None:
			print 'Player', p.name, 'disconnects'
			p.ready = False
			reason = 'Unknown reason'
			if len(instr) >= 3:
				reason = instr[2]
		else:
			print 'Could not find player by id {0}'.format(instr[1])
	else:
		pass
#	Not handled?!?
