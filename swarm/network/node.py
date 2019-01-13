
from sys import argv
import time
import socket
import socketserver
from multiprocessing.dummy import Process as Thread, Pipe
from .piped_server import PipedThreadedServer

class Node:

		def __init__(s,
				func,
				name,
				host,
				pid,
				port,
				network ):

			s.func = func
			s.name = name
			s.host = host
			s.network = network
			s.pid = pid
			s.port = port

		def start(s):
			"""
			Starts the network server to listen for messages
			initiates connection with every node.
			after every node from config connected starts
			user function
			"""

			s._print("starting...")
			s._start_threads()
			# this is to simulate delayed start
			if s.name=="B":
				time.sleep(1)
			s._handshake(s.network)
			s._print("Connection with network established!")
			s._print("##calling user fucntion")
			ret = s.func(s)
			s._print('user func returned',ret)
			return ret

		def _handshake(s, network):
			"""
			Sends a connect signal to every node in network
			then listens for response from every node in network
			"""
			data = bytes([0])+s.__int_to_bytes(len(s.name))
			data += bytes(s.name,'utf-8')
			network = [n for n in network if n['name']!=s.name]
			names = [n['name'] for n in  network ]

			for node in network:
				while True:
					try:
						s._send_to_node( data, node)
						break
					except ConnectionRefusedError as e:
						#s._print('conn refused')
						time.sleep(0.01)

			while len(names):
				msg = s.server_pipe.recv()
				msg_type = int(msg[0])
				if msg_type==0:
					name = msg[3:].decode('utf-8')
					s._print('got connection from',name)
					names.remove(name)
				else:
					s._print("warning: got unwanted message")


		def _start_threads(s):
			s.server_pipe, pipe_end = Pipe(duplex=False)
			s.server = PipedThreadedServer(s.port, pipe_end)

		def _print(s,*args):
			print("<<node %s:"%s.name,*args)

		def _get_node_by_name(s,name):
			r = [n for n in s.network if n['name']==name]
			assert len(r)==1, 'Wrong network info in node'+s.name
			return r[0]

		def _send_to_node(s, data, node):
			host = node['host']
			port = node['port']
			#s._print('sending to'+host+':'+str(port))

			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.connect((host, int(port) ))
				sock.sendall(data)
				sock.shutdown(socket.SHUT_RDWR)

		def __int_to_bytes(s,i):
			# TODO: this should belong somewhere to "utils" file
			least = i%256
			big = i//256
			return bytes([big,least])
		def __bytes_to_int(s,b):
			# TODO: this should belong somewhere to "utils" file
			big = b[0]
			least = b[1]
			return int(256*big+least)

		def send(s, to, data):
			node = s._get_node_by_name(to)
			# TODO: pickle the data object

			msg = bytes([3])+s.__int_to_bytes(len(data))
			msg += bytes(data,'utf-8')

			s._send_to_node(msg, node)

		def recv(s):
			msg_bytes = s.server_pipe.recv()
			#TODO: do not receive all data if mailformed message
			msg_type = msg_bytes[0]
			s._print('msg type',msg_type)
			msg_len = s.__bytes_to_int(msg_bytes[1:3])
			# now we send oly strings
			# TODO: send pickle
			return msg_bytes[3:].decode('utf-8')
