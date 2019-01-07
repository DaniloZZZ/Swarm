from sys import argv
import socket
import socketserver
from multiprocessing.dummy import Process as Thread, Pipe


class PipedThreadedServer(Thread):
	"""
	Sets the pipe that is used for sending the results of request handling
	to another process or thread because the server is run in a separate one
	"""

	class TCPServer(socketserver.TCPServer):

		def __init__(self, pipe, *args, **kwargs):
			self.pipe = pipe
			super(PipedThreadedServer.TCPServer, self).__init__(*args, **kwargs)


	class RequestHandler(socketserver.BaseRequestHandler):
		
		def handle(self):
			data = self.request.recv(1024).strip()
			self.server.pipe.send(str(data))


	def __init__(self, server_port, pipe, **kwargs): 
		super(PipedThreadedServer, self).__init__()
		self.server_port = server_port
		self.pipe = pipe
		self.daemon = True
		self.start()


	def run(self):
		with PipedThreadedServer.TCPServer(self.pipe, ("localhost", self.server_port), 
			PipedThreadedServer.RequestHandler) as server:
			server.serve_forever()
		


class Node:

	def __init__(self, my_port, their_port):
		self.my_port = my_port
		self.their_port = their_port
		self.my_host = "localhost"
		self.their_host = "localhost"
		self.recv_pipe, send_pipe = Pipe(duplex=False)
		self.server = PipedThreadedServer(self.my_port, send_pipe)
	

	def send(self, data):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((self.their_host, self.their_port))
			sock.sendall(bytes(data + "\n", "utf-8"))
			sock.shutdown(socket.SHUT_RDWR)

	def recv(self):
		return self.recv_pipe.recv()

