# coding:utf-8
import socket
import sys
import json
import uuid 
import time 
from threading import Thread, Lock

if(sys.version[:1] == "3"):
	import queue as Queue
	from _thread import *
else:
	import Queue
	from thread import *

class Config:
	SOCKET_HOST = '127.0.0.1'	# Symbolic name meaning all available interfaces
	SOCKET_PORT = 6688	# Arbitrary non-privileged port
	MAX_WAITING_TIME = 3600
	MAX_THNIKING_TIME = 60

class Client:
	def __init__(self, conn, addr, name, side, time):
		self.conn = conn
		self.addr = addr
		self.name = name
		self.side = side
		self.time = time

mutex = Lock()
mutex_playing = Lock()

playing_ones = {}
waiting_players = Queue.Queue()
#init queues 
#for games in range(1, 10):
#	waiting_players[games] = Queue.Queue()

def load_config():
	with open('config.txt', 'r') as f:
		for line in f.readlines():
			line = line.strip()
			if line.find('SOCKET_HOST=') >= 0:
				Config.SOCKET_HOST = line[line.index('=') + 1 : ]
			elif line.find('SOCKET_PORT=') >= 0:
				Config.SOCKET_PORT = int(line[line.index('=') + 1 : ])
			elif line.find('MAX_WAITING_TIME=') >= 0:
				Config.MAX_WAITING_TIME = int(line[line.index('=') + 1 : ])
			elif line.find('MAX_THNIKING_TIME=') >= 0:
				Config.SOCMAX_THNIKING_TIME = int(line[line.index('=') + 1 : ])
			else:
				pass

def get_counterpart_from(waiting_ones):
	counterpart = None
	mutex.acquire()
	if not waiting_ones.empty():
		counterpart = waiting_ones.get() 
	mutex.release()
	return counterpart

def to_wait_in_queue(client, the_queue):
	mutex.acquire()
	the_queue.put(client)
	mutex.release()

def send_msg_to(client, msg):
	packet = json.dumps(msg)
	if (sys.version[:1] == "3"):
		packet = packet.encode('utf-8')
	client.conn.send(packet)	

def __start_match_between(client0, client1):
	match_uuid = str(uuid.uuid4())
	mutex_playing.acquire()
	playing_ones[match_uuid] = (client0, client1)
	mutex_playing.release()

	client0.side = 0
	client0.time = Config.MAX_THNIKING_TIME
	client1.side = 1
	client1.time = Config.MAX_WAITING_TIME

	msg0 = {
		"status": 1,
		"counterpart_name": client1.name,
		"game_id": match_uuid,
		"side": client0.side,
	}
	send_msg_to(client0, msg0)
	msg1 = {
		"status": 1,
		"counterpart_name": client0.name,
		"game_id": match_uuid,
		"side": client1.side,
	}
	send_msg_to(client1, msg1)

def join_game_handler(msg, addr, conn):
	new_client = Client(conn, addr, msg['name'], -1, -1)
	#game_type = msg["id"]	
	#the_queue = waiting_players[game_type]
	counterpart = get_counterpart_from(waiting_players)
	if not counterpart: #wait 
		to_wait_in_queue(new_client, waiting_players)
		return 
	else:
		#counterpart=get_counterpart_from(waiting_players[game_type])
		__start_match_between(new_client, counterpart)

def quit_game_handler(msg):
	match_uuid = msg['game_id']
	pairs = None
	mutex_playing.acquire()
	if (match_uuid in playing_ones):
		pairs = playing_ones[match_uuid]
		del playing_ones[match_uuid]
	mutex_playing.release()

	if pairs is not None:
		if(pairs[0].side == msg['side']):
			to_notify = pairs[1]
		else:
			to_notify = pairs[0]
		msg = {
			"status": 2, #exit
			"game_id": match_uuid,
		}
		send_msg_to(to_notify, msg)

def timer_thread():
	while True:
		time.sleep(1)
		mutex_playing.acquire()
		for game_id in list(playing_ones.keys()):
			(client0, client1) = playing_ones[game_id]
			#print("%d - %d" % (client0.time, client1.time))
			if (client0.time == 0 or client1.time == 0):
				msg = {
					"status": 2, #exit
					"game_id": game_id,
				}
				send_msg_to(client0, msg)
				send_msg_to(client1, msg)
				del playing_ones[game_id]
			else:
				client0.time -= 1
				client1.time -= 1
		mutex_playing.release()

def transfer_message(msg):
	match_uuid = msg['game_id']
	pairs = playing_ones[match_uuid]
	if(pairs[0].side == msg['side']):
		to_notify = pairs[1]
		pairs[0].time = Config.MAX_WAITING_TIME
	else:
		to_notify = pairs[0]
		pairs[1].time = Config.MAX_WAITING_TIME
	to_notify.time = Config.MAX_THNIKING_TIME
	send_msg_to(to_notify, msg)

def client_thread(conn, addr):
	while True:
		data = conn.recv(1024)
		if not data:
			break
		print(data)
		data = json.loads(data)

		if not 'type' in data:
			transfer_message(data['msg'])
			continue
		if data['type'] == 0:
			join_game_handler(data['msg'], addr, conn)
			continue	
		elif data['type'] == 2:
			quit_game_handler(data['msg'])
			break
		elif data['type'] == 3:
			break
		else:
			#delivering message between the two clients
			transfer_message(data['msg'])	
			continue	
	#came out of loop
	conn.close()

def main():
	load_config()
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Socket server created')
	#try:
	server.bind((Config.SOCKET_HOST, Config.SOCKET_PORT))
	#except (socket.error, msg):
	#	print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	#	sys.exit()
		
	print('Socket bind complete')
	server.listen(10)
	print('Socket now listening')

	#now keep talking with the client
	start_new_thread(timer_thread, ())
	while True:
	    #wait to accept a connection - blocking call
		conn, addr = server.accept()
		print ('Connected with ' + addr[0] + ':' + str(addr[1]))
		
		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(client_thread, (conn, addr))
	server.close()

if __name__ == '__main__':
	main()
	